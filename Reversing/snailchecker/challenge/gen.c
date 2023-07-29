#include <stdio.h>


int josephus(int n, int k) {
    if (n == 1)
        return 0;
    if (k == 1)
        return n-1;
    if (k > n)
        return (josephus(n-1, k) + k) % n;
    int cnt = n / k;
    int res = josephus(n - cnt, k);
    res -= n % k;
    if (res < 0)
        res += n;
    else
        res += res / (k - 1);
    return res;
}
int main()
{
  char a[] = "ictf{josephus_problem_speed_boooooooost}";
  for (int i=0; i<sizeof(a)/4; i++)
    printf("%08x", josephus(((int*)a)[i], 2));
  puts("");
}

