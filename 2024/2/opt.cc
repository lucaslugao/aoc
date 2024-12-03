#include <bits/stdc++.h>
#include <cmath>
#include <cstdio>
#include <vector>

bool valid(const std::vector<int> &row, ssize_t skip = -1) {
  size_t n = row.size();
  if (n < 2 + (skip != -1))
    return false;

  ssize_t prev = -1;
  int pdiff = 0;

  for (size_t i = 0; i < n; ++i) {
    if (i == skip)
      continue;

    if (prev == -1) {
      prev = i;
      continue;
    }

    int diff = row[i] - row[prev];

    if (diff == 0 || diff < -3 || diff > 3)
      return false;

    if (pdiff == 0)
      pdiff = diff;
    else if (pdiff * diff <= 0)
      return false;

    prev = i;
  }
  return true;
}

bool valid_ignoring_one(const std::vector<int> &row) {
  for (ssize_t i = 0; i < row.size(); ++i) {
    if (valid(row, i))
      return true;
  }
  return false;
}

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  int solution1 = 0, solution2 = 0;
  int num;
  char ch;
  std::vector<int> row;

  while (true) {
    row.clear();
    while (scanf("%d%c", &num, &ch) == 2) {
      row.push_back(num);
      if (ch == '\n' || ch == '\r')
        break;
    }

    if (row.empty())
      break;

    auto v = valid(row);

    solution1 += v;
    solution2 += v || valid_ignoring_one(row);

    if (feof(stdin))
      break;
  }

  printf("%d\n", solution1);
  printf("%d\n", solution2);

  return 0;
}
