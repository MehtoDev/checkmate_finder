# checkmate_finder
 
This little program takes in a chess position where white has a mate-in-one on the board and finds the move that will result in checkmate. The program is a CLI tool that takes in the board position as a string representation and outputs the starting and ending square for the move resulting in checkmate. The uppercase letters describe positions of white pieces and lowercase letters describe positions of black pieces, '.' describe empty squares.

In the current Implementation the program assumes that neither side has en passant and neither side can castle. I enjoyed working on the problem and I have plans to implement en passant and castling in the future.

Example position:
........
.....p..
...p....
b...Q.K.
k.nq....
p..NR..r
..P..P..
R..Bn...

Example output:
e5e8