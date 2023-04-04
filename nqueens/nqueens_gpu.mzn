% N-Queens
include "alldifferent.mzn";
include "minicpp.mzn";

% Data
% ---
% Size of the chessboard
int: n;                                 

% Variables
% ---
% Chessboard's columns
array [1..n] of var 1..n: q;

% Constraints
% ---
% No queens in the same row
constraint alldifferent(q):: gpu;
% No queens in the same diagonal
constraint alldifferent(i in 1..n)(q[i] + i) ::gpu;
constraint alldifferent(i in 1..n)(q[i] - i) ::gpu;

% Search
% ---
solve :: int_search(q, input_order, indomain_min, complete) satisfy;

% Output
% ---
output ["Solution = \(q)\n"]; 
