#include <stdio.h>

double recursion3(double x, int n, int i, double f) {

    if (i == 1) {
        f = (x - 1) / x;
    } else {
        f = f * (i - 1) * (x - 1) / (i * x);
    }
    printf("F(%d) = %lf\n", i, f);
    if (i == n) {
        return f;
    }
    return f + recursion3(x, n, i + 1, f);
}

int main() {
    double x;
    int n;

    printf("Enter x:");
    scanf("%lf", &x);
    printf("Enter n:");
    scanf("%d", &n);

    printf("Sum of the first %d elements: %lf", n, recursion3(x, n, 1, 0));

}