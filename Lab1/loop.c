#include <stdio.h>

double recursionTest(double x, int n) {
    double sum = (x - 1) / x;
    double f = sum;
    for (int i = 2; i <= n; i++) {
        f = f * (i - 1) * (x - 1) / (i * x);
        sum += f;
    }
    return sum;
}

int main() {
    double x;
    int n;

    printf("Enter x:");
    scanf("%lf", &x);
    printf("Enter n:");
    scanf("%d", &n);

    printf("Sum of the first %d elements: %lf", n, recursionTest(x, n));

    return 0;
}
