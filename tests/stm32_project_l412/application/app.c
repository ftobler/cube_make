/*
 * app.c
 *
 *  Created on: Jul 11, 2025
 *      Author: ftobler
 */


#include "app.h"
#include "main.h"
#include "stdint.h"
#include "test.h"


volatile uint32_t test1 = 0;



void app_init() {
	test_fn();
	test1 = 2;
}


void app_loop() {

}
