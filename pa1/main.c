#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/wait.h>
#include "pa1.h"
#include "ipc.h"
#include "common.h"


#define PROCESS_MAX 15


int pro_num;
int fd[PROCESS_MAX+1][PROCESS_MAX+1][2];


int send(void * self, local_id dst, const Message * msg){
	
    local_id src  = *((local_id*)self);
    if (src == dst) return -1;
    int fd1   = fd[src][dst][1];
    return write(fd1, msg, sizeof(MessageHeader) + msg->s_header.s_payload_len);
	
}
int receive(void *self, local_id from, Message *msg) {
    
    local_id dst  = *((local_id*)self);
    if (dst == from) return -1;
    int fd1   = fd[from][dst][0];
    int read_result = read(fd1, msg, sizeof(Message));
    if (read_result < 0) {
        perror("read");
        return -1;
    }
    return read_result > 0 ? 0 : -1;
}
int send_multicast(void * self, const Message * msg) {
	for (local_id i = 0; i <= pro_num; i++) {
        send(self, i, msg);
		//printf("===%s",msg->s_payload);
    }
    return 0;
}
int receive_any(void *self , Message *msg){
    for(int i = 0 ; i < pro_num ; i++){
        if(receive(self, i, msg) == 0)
            return 0;
    }
    return -1;
}
int done_work(local_id pid, FILE *pipes_log, FILE *events_log){
	size_t len;
	len = fprintf(events_log,log_done_fmt,pid);
	Message msg;
	msg.s_header.s_magic = MESSAGE_MAGIC;
    msg.s_header.s_payload_len = len;
    msg.s_header.s_type = DONE;
	if(pid!=0)
		send_multicast(&pid, &msg);
	for (local_id i = 1; i <= pro_num; i++) {
       if (i != pid)
           while(receive(&pid, i, &msg) != 0);
    }
	fprintf(events_log, log_received_all_done_fmt, pid);
	
	return 1;
	
}
int start_init(local_id pid, FILE *pipes_log, FILE *events_log){
	
	size_t len;
	len = fprintf(events_log,log_started_fmt, pid, getpid(), getppid());
	Message msg;
	msg.s_header.s_magic = MESSAGE_MAGIC;
    msg.s_header.s_payload_len = len;
    msg.s_header.s_type = STARTED;
	if(pid!=0)
	send_multicast(&pid, &msg);
	
	for (local_id i = 1; i <= pro_num; i++) {
       if (i != pid)
           while(receive(&pid, i, &msg) != 0);
    }
	
	
	fprintf(events_log, log_received_all_started_fmt, pid);
	done_work(pid, pipes_log, events_log);
	return 1;
}

int close_fd(local_id id, FILE *pipes_log, int fd[PROCESS_MAX+1][PROCESS_MAX+1][2]){
	for (local_id m = 0; m <= pro_num; m++){
		for(local_id n = 0; n <= pro_num; n++){
			
			if (m != n) {
				if (m == id) {
					close(fd[m][n][0]);
					fprintf(pipes_log, "PID:%d closed read: %hhd -- %hhd\n", id , m , n);
				}

				if (n == id) {
					close(fd[m][n][1]);
					fprintf(pipes_log, "PID:%d closed write: %hhd -- %hhd\n", id , m , n);
				}

				if (m != id && n != id) {
					close(fd[m][n][0]);
					close(fd[m][n][1]);
					fprintf(pipes_log, "PID:%d closed pipe: %hhd -- %hhd\n", id , m , n);
				}
			}
		}
	}
	
	fprintf(pipes_log, "PID:%d closed all file descriptors.\n", id);
	
}
int main(int argc, char **argv){
	if(argc<2){
		printf("param is not correct!");
		return -1;
	}
	
	pro_num = atoi(argv[2]); 
	if(pro_num < 0) return -1;
	
	FILE *pipes_log = NULL;
	FILE *events_log = NULL;
	pipes_log = fopen("pipes.log","w");
	if(pipes_log == NULL){
		 perror("can't open/create pipes.log file (fopen)");
		return -1;
	}
	events_log = fopen("events.log","w+");
	if(events_log == NULL){
		 perror("failed open events.log file");
		return -1;
	}
	
	for(int i = 0; i<=pro_num;i++){
		for(int j =1;j<=pro_num;j++){
			if(i==j){
				fd[i][j][0]=-1;
				
				fd[i][j][1]=-1;
			}
			if (pipe(fd[i][j]) < 0) {
				printf("error: make ipc channel fail!\n");
				exit(1);
			}
			//fprintf(events_log, "Pipe number%d and %d was created.\n",i,j);
			
		}
		
		
	}
	int i =0;
	
	local_id pid;
	
	while(i < pro_num){
		pid = fork();
		if(pid==0){
			//child_id[i+1] = getpid();
			//fprintf(events_log,log_started_fmt, i+1,getpid(),getppid());
			int r = start_init(i+1,pipes_log,events_log);
			if(r!=1){
				//fprintf(events_log,"Process %d creat failed.\n", pid);
			}
			
			
			break;
		}
		//parent_id = getpid();
		i++;
	}
	
	/**
	if(!pid){
		fprintf(events_log,"I'm the %d child process.\n", i+1);
	}else if(pid > 0){
		fprintf(events_log,"I'm the parent process %d.\n", 0);
	}
	**/
	sleep(i);
	if(pid>0){
		int r = start_init(0,pipes_log,events_log);
		if(r!=1){
			return -1;		
		}
	
		
	}
	while(wait(NULL) > 0);
	close_fd(0, pipes_log, fd);
	
	fclose(pipes_log);
	fclose(events_log);
	return 0;
}

