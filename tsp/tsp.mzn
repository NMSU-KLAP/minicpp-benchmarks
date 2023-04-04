% Travelling Salesman Problem
include "circuit.mzn";

% Data
% ---
% Number of cities
int: C; 
% Distance city-city
array[1..C,1..C] of int: distance;

% Variables
% ---
array[1..C] of var 1..C: nextCity;
array[1..C] of var int: distNextCity;
var int: obj;

% Constraints
% ---
% The route must visits each city one time and returns to the origin city
constraint circuit(nextCity) ::domain;
% Route cost to minimize
constraint forall(i in 1..C)(distNextCity[i] = distance[i,nextCity[i]]);
constraint obj = sum(distNextCity);

% Search
% ---
solve :: int_search(nextCity, first_fail, indomain_min, complete) minimize obj;

% Output
% ---
output ["Solution = \(nextCity)\nObjective = \(obj)\n"]; 