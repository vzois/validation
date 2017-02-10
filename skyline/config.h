#ifndef CONFIG_H
#define CONFIG_H

//Dataset Configuration
#define DATA_N 131072
#define DPUS 2
#define N (DATA_N / DPUS)
#define D 4
#define K 128
#define BVECTOR_N (N >> 5) // N/32 Bit vectors

////////////////////////////////////////////////
//radixselect Runtime Configuration
#define BUFFER 256
#define BINS 17
#define TASKLETS 16
#define ACC_BUCKET 0

//Radix Select Addresses
#define DATA_ADDR 0x1000
#define BUCKET_ADDR (DATA_ADDR + (N << 2))

//Radix Select Type
#define CSELECT 0x1000
#define CWINDOW 0x1001

////////////////////////////////////////////
//kskyline Runtime Configuration
////////////////////////////////////////////
#define WRAM_BUFFER 256 //Part of the buffer for each tasklet to store the window// 16 tasklets = 16*256 bytes // Window cannot be larger that 4096 bytes
#define WRAM_BUFFER_SHF 8 //log256 = 8
#define WINDOW_SIZE (K*D)
#define WINDOW_SIZE_BYTES (WINDOW_SIZE << 2) //Total window size//Assume that points fit in WRAM
#define TASKLET_LOAD (WINDOW_SIZE_BYTES >> WRAM_BUFFER_SHF) //Which tasklets participate in the window load//Determines also size of shared wram window
#define VALUES_PER_BUFFER (WRAM_BUFFER >> 2)//Values that can fit into buffer // 256 bytes -> 64 32 bit values
#define POINTS_PER_BUFFER (VALUES_PER_BUFFER / D)//How many points fit into a single buffer load // Less points as we increase point dimensions//

//kskyline Addresses
#define POINTS_ADDR 0x1000
#define WINDOW_ADDR (POINTS_ADDR + ((N * D)<<2))
#define RANK_ADDR (POINTS_ADDR + ((K * D)<<2))
#define MASK_ADDR 0x3000000

//General Runtime Addresses
#define VAR_0_ADDR 0x0
#define VAR_1_ADDR 0x4
#define VAR_2_ADDR 0x8
#define VAR_3_ADDR 0xC
#define VAR_4_ADDR 0x10
#define VAR_5_ADDR 0x14
#define VAR_6_ADDR 0x18
#define VAR_7_ADDR 0x1C

#endif
