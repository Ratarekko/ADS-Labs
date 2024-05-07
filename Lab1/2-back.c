#include <stdio.h>

struct Result {
    double sum;
    double f;
};

struct Result recursion2(double x, int n) {
    struct Result result;

    //printf("Entering recursion with n = %d\n", n);

    if (n == 1) {
        result.sum = (x - 1) / x;
        result.f = result.sum;
        printf("F(%d) = %lf\n", n, result.f);
        //printf("Leaving recursion with n = %d\n", n);
        return result;
    }

    result = recursion2(x, n - 1);
    result.f *= ((n - 1) * (x - 1)) / (n * x);
    result.sum += result.f;

    printf("F(%d) = %lf\n", n, result.f);
    printf("Current sum = %lf\n", result.sum);
    //printf("Leaving recursion with n = %d\n", n);

    return result;
}

int main() {
    double x;
    int n;

    printf("Enter x:");
    scanf("%lf", &x);
    printf("Enter n:");
    scanf("%d", &n);

    struct Result result = recursion2(x, n);

    printf("Sum of the first %d elements: %lf", n, result.sum);

    return 0;
}
