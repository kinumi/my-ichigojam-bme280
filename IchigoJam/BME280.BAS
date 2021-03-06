1 'BME280 sensor

10 W="ambient channel"
20 X="ambient writekey"
30 Y=30
40 Z="server address"

110 GSB@SETUP
120 ?"MJ POST START ";STR$(Z):LED1
130 ?STR$(W)
140 ?STR$(X)
150 GSB@CARIB
160 FORI=0TO31:?PEEK(#800+I):NEXT
170 GSB@DATA
180 FORI=0TO7:?PEEK(#800+I):NEXT
190 ?"MJ POST END":LED0
200 WAIT Y*60
999 GOTO120

1010 @I2CR
1020 [101]=I2CR(#76,#8C6,1,#8C8,1)
1999 RETURN
2010 @I2CW
2020 [101]=I2CW(#76,#8C6,1,#8C8,1)
2999 RETURN

3010 @SETUP
3020 A=#8C6:B=#8C8:C=0
3030 POKEA,#F2:POKEB,`00000101:GSB@I2CW
3040 POKEA,#F4:POKEB,`10110111:GSB@I2CW
3050 POKEA,#F5:POKEB,`10100000:GSB@I2CW
3999 RETURN

4010 @CARIB
4020 A=#8C6:B=#8C8:C=0
4030 FOR I=0 TO 23
4040 POKEA,#88+I:GSB@I2CR
4050 POKE#800+C,PEEK(B)
4060 C=C+1
4070 NEXT
4080 POKEA,#A1:GSB@I2CR
4090 POKE#800+C,PEEK(B)
4100 C=C+1
4110 FOR I=0 TO 7
4120 POKEA,#E1+I:GSB@I2CR
4130 POKE#800+C,PEEK(B)
4140 C=C+1
4150 NEXT
4999 RETURN

5010 @DATA
5020 A=#8C6:B=#8C8:C=0
5030 POKEA,#F3:GSB@I2CR
5040 IF PEEK(B)&`00001000!=0 GOTO5030
5050 FOR I=0 TO 7
5060 POKEA,#F7+I:GSB@I2CR
5070 POKE#800+I,PEEK(B)
5080 NEXT
5999 RETURN
