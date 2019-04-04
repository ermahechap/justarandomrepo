/*
Convex Hull, Graham-Scan with Monotone Chain
https://open.kattis.com/problems/convexhull
*/

#include<bits/stdc++.h>
#define ll long long
#define pii pair<int,int>
#define x first
#define y second
#define EPS 1e-9
#define ori(O,A) {A.x - O.x , A.y - O.y}

using namespace std;

int sgn_cross(pii A, pii B){
    ll cross = (A.x * B.y) - (B.x * A.y);
    return (cross<0)? -1 : (cross>0)? 1 : 0;
}

int main(){
    int n;
    while(cin>>n && n!=0){
        vector<pii> dat(n,{0,0});
        for(int i = 0 ; i< n; i++){
            cin>>dat[i].x>>dat[i].y;
        }
        sort(dat.begin(),dat.end());
        dat.erase(unique(dat.begin(),dat.end()),dat.end());
        n = dat.size();
        if(n<=2){
            cout<<n<<'\n';
            for(pii a: dat)cout<<a.x<<' '<<a.y<<'\n';
            continue;
        }
        vector<pii>A(2*n,{0,0}); int k = 0;

        for(int i = 0 ; i<n ; i++){
            while(k>=2 && sgn_cross(ori(A[k-2],A[k-1]), ori(A[k-2],dat[i]))<=0)k--;
            A[k++] = dat[i];
        }
        int low = k+1;
        for(int i = n-2; i>=0 ; i--){
            while(k>=low && sgn_cross(ori(A[k-2],A[k-1]), ori(A[k-2],dat[i]))<=0)k--;
            A[k++] = dat[i];
        }

        cout<<k-1<<'\n';
        for(int i = 0 ; i <k-1;i++){
            cout<<A[i].x<<' '<<A[i].y<<'\n';
        }
    }
}