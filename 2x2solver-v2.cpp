#include <bits/stdc++.h>

using namespace std;

string state, target;
string faces = "ULFRBD";
vector<string> solution;
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
    for(auto m : solution) cout << m << " ";
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

string decodestate(uint64_t x) {
    const char colors[] = {'W', 'Y', 'O', 'R', 'G', 'B'};
    string state(24, ' ');
    for (int i = 23; i >= 0; i--) {
        state[i] = colors[x % 6];
        x /= 6;
    }
    return state;
}

void solve(){
    unordered_set<uint64_t> visited;
    unordered_map<uint64_t, pair<uint64_t, string>> parent;
    queue<pair<uint64_t, int>> bfs;
    uint64_t estate = encodestate(state), newestate;
    bfs.push({estate, -1});
    visited.insert(estate);

    while(!bfs.empty()){
        auto [estate, lastmove] = bfs.front();
        bfs.pop();
        state = decodestate(estate);

        if(state == target) break;

        if(lastmove != 0){
            R();
            newestate = encodestate(state);
            if(visited.find(newestate) == visited.end()){
                bfs.push({newestate, 0});
                visited.insert(newestate);
                parent[newestate] = {estate, "R"};
            }

            R();
            newestate = encodestate(state);
            if(visited.find(newestate) == visited.end()){
                bfs.push({newestate, 0});
                visited.insert(newestate);
                parent[newestate] = {estate, "R2"};
            }
            
            R();
            newestate = encodestate(state);
            if(visited.find(newestate) == visited.end()){
                bfs.push({newestate, 0});
                visited.insert(newestate);
                parent[newestate] = {estate, "R'"};
            }
            R();
        }
        
        if(lastmove != 1){
            U();
            newestate = encodestate(state);
            if(visited.find(newestate) == visited.end()){
                bfs.push({newestate, 1});
                visited.insert(newestate);
                parent[newestate] = {estate, "U"};
            }

            U();
            newestate = encodestate(state);
            if(visited.find(newestate) == visited.end()){
                bfs.push({newestate, 1});
                visited.insert(newestate);
                parent[newestate] = {estate, "U2"};
            }
            
            U();
            newestate = encodestate(state);
            if(visited.find(newestate) == visited.end()){
                bfs.push({newestate, 1});
                visited.insert(newestate);
                parent[newestate] = {estate, "U'"};
            }
            U();
        }
        
        if(lastmove != 2){
            F();
            newestate = encodestate(state);
            if(visited.find(newestate) == visited.end()){
                bfs.push({newestate, 2});
                visited.insert(newestate);
                parent[newestate] = {estate, "F"};
            }

            F();
            newestate = encodestate(state);
            if(visited.find(newestate) == visited.end()){
                bfs.push({newestate, 2});
                visited.insert(newestate);
                parent[newestate] = {estate, "F2"};
            }
            
            F();
            newestate = encodestate(state);
            if(visited.find(newestate) == visited.end()){
                bfs.push({newestate, 2});
                visited.insert(newestate);
                parent[newestate] = {estate, "F'"};
            }
            F();
        }
    }

    uint64_t currestate = encodestate(target);
    while(parent.find(currestate) != parent.end()){
        solution.push_back(parent[currestate].second);
        currestate = parent[currestate].first;
    }
    reverse(solution.begin(), solution.end());
}

int main(){

    // getinput();
    state = "WWWWOOOOGGGGRRRRBBBBYYYY";

    R();
    U();
    F();
    R2();
    U2();
    F2();
    Rp();
    Fp();
    Up();
    R();
    U();

    findtarget();
    solve();
    printsolution();

    return 0;
}
