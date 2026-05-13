#include <bits/stdc++.h>

using namespace std;

string state, target;
string faces = "ULFRBD";
string solution[11];
bool found = 0;
int usedmoves;
unordered_set<uint64_t> visited;
map<char, char> opposite = {
    {'W', 'Y'},
    {'Y', 'W'},
    {'O', 'R'},
    {'R', 'O'},
    {'G', 'B'},
    {'B', 'G'}
};


void R(){
    state = string() + state[0]+state[9]+state[2]+state[11] + state[4]+state[5]+state[6]+state[7] + state[8]+state[21]+state[10]+state[23]
    + state[14]+state[12]+state[15]+state[13] + state[3]+state[17]+state[1]+state[19] + state[20]+state[18]+state[22]+state[16];
}

void R2(){
    state = string() + state[0]+state[21]+state[2]+state[23] + state[4]+state[5]+state[6]+state[7] + state[8]+state[18]+state[10]+state[16]
    + state[15]+state[14]+state[13]+state[12] + state[11]+state[17]+state[9]+state[19] + state[20]+state[1]+state[22]+state[3];
}

void Rp(){
    state = string() + state[0]+state[18]+state[2]+state[16] + state[4]+state[5]+state[6]+state[7] + state[8]+state[1]+state[10]+state[3]
    + state[13]+state[15]+state[12]+state[14] + state[23]+state[17]+state[21]+state[19] + state[20]+state[9]+state[22]+state[11];
}

void U(){
    state = string() + state[2]+state[0]+state[3]+state[1] + state[8]+state[9]+state[6]+state[7] + state[12]+state[13]+state[10]+state[11]
    + state[16]+state[17]+state[14]+state[15] + state[4]+state[5]+state[18]+state[19] + state[20]+state[21]+state[22]+state[23];
}

void U2(){
    state = string() + state[3]+state[2]+state[1]+state[0] + state[12]+state[13]+state[6]+state[7] + state[16]+state[17]+state[10]+state[11]
    + state[4]+state[5]+state[14]+state[15] + state[8]+state[9]+state[18]+state[19] + state[20]+state[21]+state[22]+state[23];
}

void Up(){
    state = string() + state[1]+state[3]+state[0]+state[2] + state[16]+state[17]+state[6]+state[7] + state[4]+state[5]+state[10]+state[11]
    + state[8]+state[9]+state[14]+state[15] + state[12]+state[13]+state[18]+state[19] + state[20]+state[21]+state[22]+state[23];
}

void F(){
    state = string() + state[0]+state[1]+state[7]+state[5] + state[4]+state[20]+state[6]+state[21] + state[10]+state[8]+state[11]+state[9]
    + state[2]+state[13]+state[3]+state[15] + state[16]+state[17]+state[18]+state[19] + state[14]+state[12]+state[22]+state[23];
}

void F2(){
    state = string() + state[0]+state[1]+state[21]+state[20] + state[4]+state[14]+state[6]+state[12] + state[11]+state[10]+state[9]+state[8]
    + state[7]+state[13]+state[5]+state[15] + state[16]+state[17]+state[18]+state[19] + state[3]+state[2]+state[22]+state[23];
}

void Fp(){
    state = string() + state[0]+state[1]+state[12]+state[14] + state[4]+state[3]+state[6]+state[2] + state[9]+state[11]+state[8]+state[10]
    + state[21]+state[13]+state[20]+state[15] + state[16]+state[17]+state[18]+state[19] + state[5]+state[7]+state[22]+state[23];
}

void getinput(){
    for(auto face : faces){
        char ch;
        cout << face << " face:" << endl;
        for(int i = 0; i < 4; i++){
            cin >> ch;
            state += toupper(ch);
        }
    }
}

void findtarget(){
    target += string(4, opposite[state[22]]);
    target += string(4, state[6]);
    target += string(4, opposite[state[19]]);
    target += string(4, opposite[state[6]]);
    target += string(4, state[19]);
    target += string(4, state[22]);
}

void printsolution(){
    for(int i = 0; i < usedmoves; i++) cout << solution[i] << " ";
    cout << endl;
}

uint64_t encodestate(const string& state) {
    uint64_t x = 0;
    for (char c : state) {
        x = x * 6 + (c == 'W' ? 0 :
                     c == 'Y' ? 1 :
                     c == 'O' ? 2 :
                     c == 'R' ? 3 :
                     c == 'G' ? 4 : 5);
    }
    return x;
}


void solve(int move, int lastmove){
    uint64_t estate = encodestate(state);
    if(visited.find(estate) != visited.end()) return;
    if(state == target){
        found = 1;
        usedmoves = move;
        return;
    }
    if(move == 11) return;
    visited.insert(estate);

    if(lastmove != 0){
        R();
        solution[move] = "R";
        solve(move+1, 0);
        if(found) return;

        R();
        solution[move] = "R2";
        solve(move+1, 0);
        if(found) return;

        R();
        solution[move] = "R'";
        solve(move+1, 0);
        if(found) return;
        R();
    }

    if(lastmove != 1){
        U();
        solution[move] = "U";
        solve(move+1, 1);
        if(found) return;

        U();
        solution[move] = "U2";
        solve(move+1, 1);
        if(found) return;

        U();
        solution[move] = "U'";
        solve(move+1, 1);
        if(found) return;
        U();
    }
    
    if(lastmove != 2){
        F();
        solution[move] = "F";
        solve(move+1, 2);
        if(found) return;

        F();
        solution[move] = "F2";
        solve(move+1, 2);
        if(found) return;

        F();
        solution[move] = "F'";
        solve(move+1, 2);
        if(found) return;
        F();
    }
}

int main(){
    
    getinput();
    findtarget();
    solve(0, -1);
    printsolution();
    
    return 0;
}
