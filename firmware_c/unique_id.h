/*
 *
 *
 */
#include <stdint.h>

struct u_id {
    uint16_t off0;
    uint16_t off2;
    uint32_t off4;
    uint32_t off8;
};

// Read U_ID register 
void unique_id_read(struct u_id *id);

