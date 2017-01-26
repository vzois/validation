#include<meetpoint.h>

//Vector Dataset Configuration
#define N 524288
#define K 32768

//Runtime Configuration
#define BUFFER 256
#define BINS 17
#define TASKLETS 16

//Address in MRAM
#define RANK_ADDR 0x0

void barrier_wait(uint8_t id){
	meetpoint_t mtp = meetpoint_get(0);
	if(id < 1){
		meetpoint_notify(mtp);
	}else{
		meetpoint_subscribe(mtp);
	}
}
