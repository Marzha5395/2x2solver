#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <queue>
#include <map>

using namespace std;

#define pii pair<int,int>

string state, target;
string faces = "ULFRBD";
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
    state = string() + state[0]+state[16]+state[2]+state[18] + state[4]+state[5]+state[6]+state[7] + state[8]+state[1]+state[10]+state[3]
    + state[13]+state[15]+state[12]+state[14] + state[23]+state[17]+state[21]+state[19] + state[20]+state[9]+state[22]+state[11];
}

void U(){
    state = string() + state[3]+state[0]+state[2]+state[1] + state[8]+state[9]+state[6]+state[7] + state[12]+state[13]+state[10]+state[11]
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
    state = string() + state[0]+state[1]+state[7]+state[5] + state[4]+state[20]+state[6]+state[21] + state[9]+state[11]+state[8]+state[10]
    + state[2]+state[13]+state[3]+state[15] + state[16]+state[17]+state[18]+state[19] + state[12]+state[14]+state[22]+state[23];
}

void F2(){
    state = string() + state[0]+state[1]+state[21]+state[20] + state[4]+state[14]+state[6]+state[12] + state[11]+state[10]+state[9]+state[8]
    + state[7]+state[13]+state[5]+state[15] + state[16]+state[17]+state[18]+state[19] + state[3]+state[2]+state[22]+state[23];
}

void Fp(){
    state = string() + state[0]+state[1]+state[12]+state[14] + state[4]+state[3]+state[6]+state[2] + state[10]+state[8]+state[11]+state[9]
    + state[21]+state[13]+state[20]+state[15] + state[16]+state[17]+state[18]+state[19] + state[5]+state[7]+state[22]+state[23];
}

void getinput(){
    for(auto face : faces){
        char ch;
        cout << face << " face:" << endl;
        for(int i = 0; i < 4; i++){
            cin >> ch;
            state += ch;
        }
    }
    transform(state.begin(), state.end(), state.begin(),::toupper);
}

void findtarget(){
    target += string(4, opposite[state[22]]);
    target += string(4, state[6]);
    target += string(4, opposite[state[19]]);
    target += string(4, opposite[state[6]]);
    target += string(4, state[19]);
    target += string(4, state[22]);
}


int main(){
    // getinput();
    state = "WWWWOOOOGGGGRRRRBBBBYYYY";
    findtarget();
    F2();
    F2();
    cout << state << endl;
    cout << target;
}
