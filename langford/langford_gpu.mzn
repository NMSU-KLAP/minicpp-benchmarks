% Langford's problem
include "alldifferent.mzn";
include "minicpp.mzn";

% Data
% ---
% Number of digits
int: n;
% Copies of the digits
int: m;

% Variables
% ---
% Positions of the digits
array[1..n,1..m] of var 1..m*n: x;

% Constraints
% ---
% Every digit is in a different position
constraint alldifferent([x[d,c] | d in 1..n, c in 1..m]) ::gpu;
constraint forall(d in 1..n, c in 1..m-1) (x[d,c+1] = x[d,c] + d + 1);

% Search
% ---
solve ::int_search(x, first_fail, indomain_min, complete) satisfy;

% Output
% ---
output ["Solution = \([x[d,c] | d in 1..n, c in 1..m])\n"]; 