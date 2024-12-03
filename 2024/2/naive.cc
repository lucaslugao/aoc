#include <cmath>
#include <cstdio>
#include <vector>

bool valid(const std::vector<int> &row) {
  if (row.size() < 2)
    return false;

  int initial_diff = row[1] - row[0];

  for (size_t i = 1; i < row.size(); ++i) {
    int diff = row[i] - row[i - 1];
    if (std::abs(diff) < 1 || std::abs(diff) > 3 || diff * initial_diff <= 0)
      return false;
  }
  return true;
}

bool valid_ignoring_one(const std::vector<int> &row) {
  for (size_t i = 0; i < row.size(); ++i) {
    std::vector<int> new_row = row;
    new_row.erase(new_row.begin() + i);
    if (valid(new_row))
      return true;
  }
  return false;
}

int main() {
  int solution1 = 0, solution2 = 0;
  int num;
  char ch;

  while (true) {
    std::vector<int> row;
    while (scanf("%d%c", &num, &ch) == 2) {
      row.push_back(num);
      if (ch == '\n' || ch == '\r')
        break;
    }

    if (row.empty())
      break;

    solution1 += valid(row);
    solution2 += valid_ignoring_one(row);

    if (feof(stdin))
      break;
  }

  printf("%d\n", solution1);
  printf("%d\n", solution2);

  return 0;
}
