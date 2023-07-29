#include <bits/stdc++.h>
using namespace std;
string flag;
int main() {
    string s;
    cin >> s;
    reverse(s.begin(), s.end());
    string temp = s;
    int n = s.size();
    vector<int> thing(n);
    iota(thing.begin(), thing.end(), 0);
    for (int i = 0; i< n; i++){
        for (int j = 0; j< n; j++) thing[j]= (thing[j]+i)%n;
        for (int j = 0; j< n; j++)s[j]= temp[thing[j]];
        iota(thing.begin(), thing.end(), 0);
    }
    vector<char> alpha = {'z','y','x','^','w','u','%','v','!','t','s','1','r', ';','q','@','o','p','#','n','m','$','l','k','(','i','j','g', 'h','*','f','e','d','&','c','a','0', 'b', '-', '{', '}', ')'};
    vector<char> temp1 = alpha;
    reverse(temp1.begin(), temp1.end());
    vector<char> beta = alpha;
    //cout << s<< endl;
    for(int i = 0; i < s.size(); i++){
        int ind = distance(alpha.begin(), find(alpha.begin(), alpha.end(), s[i]));
        s[i] = temp1[ind];
    }
//    cout << s;
    if (s == "oynuuvefmqjn1qlfnw$j*vmx1dv") cout << "CORRECT\n";
    else cout << "INCORRECT\n";
}
