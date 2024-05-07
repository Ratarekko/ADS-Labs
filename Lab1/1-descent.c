#include <stdio.h>

double recursion1(double x, int n, int i, double f, double sum) {
    if (i > n) {
        return sum;
    }
    if (i == 1) {
        f = (x - 1) / x;
    } else {
        f = f * (i - 1) * (x - 1) / (i * x);
    }
    printf("Current sum = %lf\n", sum);
    printf("F(%d) = %lf\n", i, f);
    sum += f;
    return recursion1(x, n, i + 1, f, sum);

}

int main() {
    double x;
    int n;

    printf("Enter x:");
    scanf("%lf", &x);
    printf("Enter n:");
    scanf("%d", &n);

    printf("\nSum of the first %d elements: %lf", n, recursion1(x, n, 1, 0, 0));

    return 0;
}