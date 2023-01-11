#include <iostream>
#include <queue>
#include <tuple>
#include <vector>

using namespace std;

class Solution {
public:
  int minTime(int n, vector<vector<int>> &edges, vector<bool> &hasApple) {
    // make a source -> dest graph repr for BFS
    vector<vector<int>> nodes(n, vector<int>());
    for (auto edge : edges) {
      int start = edge[0];
      int end = edge[1];
      nodes[start].push_back(end);
      nodes[end].push_back(start);
    }

    // get all apple nodes
    vector<int> appleNodes;
    int i = 0;
    for (auto apple : hasApple) {
      if (apple)
        appleNodes.push_back(i);
      i++;
    }

    return 0;
  }

  int minDistanceBetweenNodes(int n, vector<vector<int>> &neighbors, int start,
                              int dest) {
    vector<int> distance(n, 0);
    vector<bool> visited(n, false);
    queue<int> q;
    distance[start] = 0;

    q.push(start);
    visited[start] = true;

    while (!q.empty()) {
      int curr = q.front();
      q.pop();

      for (auto neighbor : neighbors[curr]) {
        if (visited[neighbor])
          continue;

        distance[neighbor] = distance[curr] + 1;
        q.push(neighbor);
        visited[neighbor] = true;
      }
    }

    return distance[dest];
  }
};

int main() {
  auto solution = Solution();

  vector<vector<int>> edges{{0, 1}, {0, 2}, {1, 4}, {1, 5}, {2, 3}, {2, 6}};

  vector<bool> hasApple;
  hasApple.push_back(false);
  hasApple.push_back(false);
  hasApple.push_back(true);
  hasApple.push_back(false);
  hasApple.push_back(true);
  hasApple.push_back(true);
  hasApple.push_back(false);

  solution.minTime(7, edges, hasApple);

  /* cout << "solution: " << solution.minTime(7, edges, hasApple) << endl; */
}
