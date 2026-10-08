#include <bits/stdc++.h>
using namespace std;
struct V{int x,y,z;}; struct A{double x,y,z;};
static inline long long key(int x,int y,int z){const int O=4096; return ((long long)(x+O)<<26)|((long long)(y+O)<<13)|(long long)(z+O);}
static inline long long k2(const V&v){return 1LL*v.x*v.x+1LL*v.y*v.y+1LL*v.z*v.z;}
static inline double dot(const A&a,const A&b){return a.x*b.x+a.y*b.y+a.z*b.z;}
static inline double dotq(const V&q,const A&a){return q.x*a.x+q.y*a.y+q.z*a.z;}
static inline V add(const V&a,const V&b){return {a.x+b.x,a.y+b.y,a.z+b.z};}
static inline V sub(const V&a,const V&b){return {a.x-b.x,a.y-b.y,a.z-b.z};}
struct Node{V k; A a; long long r2;};
int main(int argc,char**argv){int n=argc>1?atoi(argv[1]):3, cm=argc>2?atoi(argv[2]):4; double nu=1e-5; int L=64*n,H=63*n,N=cm*H; long long N2=1LL*N*N;
 vector<Node>S; unordered_map<long long,int> idx; idx.reserve(20000);
 auto addmode=[&](V k,int j){long long r=k2(k); double v[3]={0,0,0}; int kk[3]={k.x,k.y,k.z}; for(int i=0;i<3;i++) v[i]=r*(i==j)-1.0*kk[j]*kk[i]; V km={-k.x,-k.y,-k.z}; A a{v[0],v[1],v[2]}, an{-v[0],-v[1],-v[2]}; idx[key(k.x,k.y,k.z)]=S.size();S.push_back({k,a,r}); idx[key(km.x,km.y,km.z)]=S.size();S.push_back({km,an,r});};
 for(int i=-n;i<=n;i++)for(int j=-n;j<=n;j++)for(int l=-n;l<=n;l++)addmode({L+i,j,l},1);
 for(int i=-n;i<=n;i++)for(int j=-n;j<=n;j++)for(int l=-n;l<=n;l++)addmode({i,3*L+j,l},2);
 for(int i=-2*n;i<=2*n;i++)for(int j=-2*n;j<=2*n;j++)for(int l=-2*n;l<=2*n;l++)addmode({L+i,3*L+j,l},2);
 double E0=0; for(auto&s:S)E0+=dot(s.a,s.a); double al=1/sqrt(E0); for(auto&s:S){s.a.x*=al;s.a.y*=al;s.a.z*=al;}
 double E=0,X=0,Y=0,Z=0; for(auto&s:S){double aa=dot(s.a,s.a);E+=aa;X+=s.r2*aa;Y+=1.0*s.r2*s.r2*aa;Z+=1.0*s.r2*s.r2*s.r2*aa;}
 auto mask=[&](const V&p,const V&q,const V&k){long long a=k2(p),b=k2(q),c=k2(k);return a>1&&b>1&&c>1&&a!=b&&a!=c&&b!=c;};
 double T=0,Vv=0; for(auto&pp:S)for(auto&qq:S){V kk=add(pp.k,qq.k); auto it=idx.find(key(kk.x,kk.y,kk.z)); if(it==idx.end()||!mask(pp.k,qq.k,kk))continue; auto&ak=S[it->second]; double term=ak.r2*dotq(qq.k,pp.a)*dot(qq.a,ak.a);T+=term; Vv+=-nu*(pp.r2+qq.r2+ak.r2)*term;}
 unordered_map<long long,A> raw; raw.reserve(S.size()*10);
 for(auto&pp:S)for(auto&qq:S){V kk=add(pp.k,qq.k); long long rr=k2(kk); if(rr==0||rr>N2)continue; double s=dotq(qq.k,pp.a); auto &v=raw[key(kk.x,kk.y,kk.z)];v.x+=s*qq.a.x;v.y+=s*qq.a.y;v.z+=s*qq.a.z;}
 unordered_map<long long,A> R;R.reserve(raw.size()*2); for(auto &e:raw){long long K=e.first; int z=(K&8191)-4096,y=((K>>13)&8191)-4096,x=((K>>26)&8191)-4096; V k{x,y,z}; double rr=k2(k),kv=x*e.second.x+y*e.second.y+z*e.second.z;R[K]={e.second.x-x*kv/rr,e.second.y-y*kv/rr,e.second.z-z*kv/rr};}
 double Q=0;
 // receiver slot
 for(auto&pp:S)for(auto&qq:S){V kk=add(pp.k,qq.k); auto ir=R.find(key(kk.x,kk.y,kk.z)); if(ir==R.end()||!mask(pp.k,qq.k,kk))continue; Q+=k2(kk)*dotq(qq.k,pp.a)*dot(qq.a,ir->second);}
 // p slot q,k in S
 for(auto&qq:S)for(auto&kk:S){V p=sub(kk.k,qq.k); auto ir=R.find(key(p.x,p.y,p.z)); if(ir==R.end()||!mask(p,qq.k,kk.k))continue; Q+=kk.r2*dotq(qq.k,ir->second)*dot(qq.a,kk.a);}
 // q slot p,k in S
 for(auto&pp:S)for(auto&kk:S){V q=sub(kk.k,pp.k); auto ir=R.find(key(q.x,q.y,q.z)); if(ir==R.end()||!mask(pp.k,q,kk.k))continue; Q+=kk.r2*dotq(q,pp.a)*dot(ir->second,kk.a);}
 double U2=0;for(auto&s:S){auto ir=R.find(key(s.k.x,s.k.y,s.k.z));if(ir!=R.end())U2+=1.0*s.r2*s.r2*dot(s.a,ir->second);} double M=nu*nu/2*Z-nu/2*U2; double D=T-nu*Y/4,Dp=Q+Vv+M,tau=D/Dp,st=tau*pow((double)H,2.5);
 cout<<setprecision(15)<<"n "<<n<<" H "<<H<<" N "<<N<<" modes "<<S.size()<<" generated "<<R.size()<<"\nE "<<E<<" X "<<X<<" Y "<<Y<<" T "<<T<<" D "<<D<<" Q "<<Q<<" V "<<Vv<<" M "<<M<<" Dp "<<Dp<<" D/X "<<D/X<<" tau "<<tau<<" H25tau "<<st<<"\n";
}
