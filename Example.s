// compiled with fs65c for Darwin arm64/aarch64

.global _start
.p2align 2

_start:
	mov X0, #0x9
	str X0, [SP, #-16]!
	ldr X0, [SP], #16
	str X0, [SP, #-16]!
	str X0, [SP, #-16]!
	ldr X0, [SP], #16
	mov X0, #0x8
	str X0, [SP, #-16]!
	ldr X0, [SP], #16
	str X0, [SP, #-16]!
	str X0, [SP, #-16]!
	ldr X0, [SP], #16
	add SP, SP, 0x10
	ldr X0, [SP]
	sub SP, SP, 0x10
	str X0, [SP, #-16]!
	ldr X0, [SP], #16
	str X0, [SP, #-16]!
	str X0, [SP, #-16]!
	ldr X0, [SP], #16
	mov X0, #0x6
	str X0, [SP, #-16]!
	add SP, SP, 0x30
	ldr X0, [SP]
	sub SP, SP, 0x30
	str X0, [SP, #-16]!
	mov X0, #0x7
	str X0, [SP, #-16]!
	ldr X1, [SP], #16
	ldr X2, [SP], #16
	sub X0, X2, X1
	str X0, [SP, #-16]!
	ldr X1, [SP], #16
	ldr X2, [SP], #16
	add X0, X1, X2
	str X0, [SP, #-16]!
	ldr X0, [SP], #16
	mov X11, X0
	mov X0, X11
	mov X16, #0x1
	svc #0xffff
	ldr X0, [SP], #16
