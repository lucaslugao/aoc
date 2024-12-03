#include <algorithm>
#include <cmath>
#include <cstdio>
#include <unordered_map>
#include <vector>

int main() {
  std::vector<int> list1, list2;
  std::unordered_map<int, int> counter2;
  int a, b;
  while (scanf("%d %d", &a, &b) == 2) {
    list1.push_back(a);
    list2.push_back(b);
    counter2[b]++;
  }

  std::sort(list1.begin(), list1.end());
  std::sort(list2.begin(), list2.end());

  long long solution1 = 0, solution2 = 0;
  for (size_t i = 0; i < list1.size(); ++i) {
    solution1 += std::abs(list1[i] - list2[i]);
    solution2 += 1LL * list1[i] * counter2[list1[i]];
  }

  printf("%lld\n%lld\n", solution1, solution2);
  return 0;
}
