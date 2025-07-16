from typing import List
import collections


class LRUCache:

    def __init__(self, capacity: int):
        self.dic = collections.OrderedDict()
        self.remain = capacity

    def get(self, key: int) -> int:
        if key not in self.dic:
            return -1
        return self.dic[key]

    def put(self, key: int, value: int) -> None:
        if key in self.dic:
            self.dic.pop(key)
        else:
            if self.remain > 0:
                self.remain -= 1
            else:
                self.dic.popitem(last=False)
        self.dic[key] = value


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)


class Solution:
    def findWords(self, board, words):
        self.root = {}
        self.result = set()
        self.end = '#'
        self.dx = [-1, 0, 1, 0]
        self.dy = [0, -1, 0, 1]
        self.length_x = len(board[0])
        self.length_y = len(board)

        for word in words:
            node = self.root
            for char in word:
                node = node.setdefault(char, {})
            node[self.end] = self.end

        for y, l in enumerate(board):
            for x, char in enumerate(l):
                if char in self.root:
                    self.findWords_dfs(board, x, y, '', self.root)

        return list(self.result)

    def findWords_dfs(self, board, x, y, cur_word, cur_dict):
        cur_word += board[y][x]
        cur_dict = cur_dict[board[y][x]]

        if self.end in cur_dict:
            self.result.add(cur_word)

        tmp, board[y][x] = board[y][x], '@'
        for i in range(4):
            _x, _y = self.dx[i] + x, self.dy[i] + y
            if 0 <= _x < self.length_x and 0 <= _y < self.length_y and board[_y][_x] in cur_dict and board[_y][_x] != '@':
                self._dfs(board, _x, _y, cur_word, cur_dict)
        board[y][x] = tmp

    def climbStairs(self, n: int) -> int:
        """
        爬楼梯
        https://leetcode-cn.com/problems/climbing-stairs/
        :param n:
        :return:
        """
        if n <= 1:
            return 1
        elif n == 2:
            return 2
        arr = [0] * (n + 1)
        arr[1] = 1
        arr[2] = 2
        for i in range(3, n + 1):
            arr[i] = arr[i - 1] + arr[i - 2]
        return arr[n]

    def minimumTotal(self, triangle) -> int:
        """
        三角形最小路径和
        https://leetcode-cn.com/problems/triangle/
        triangle: List[List[int]]
        迭代的时候每次将下面两个数的最小值加上其本身保存在一个二位数组
        """
        if not triangle:
            return 0
        y = len(triangle)
        x = len(triangle[-1])
        d = [[0] * x] * y
        d[-1] = triangle[-1]
        for j in range(y - 1):
            for i in range(len(triangle[-2 - j])):
                d[-2 - j][i] = min(d[-1 - j][i], d[-1 - j][i + 1]) + triangle[-2 - j][i]
        return d[0][0]

    def maxProduct(self, nums) -> int:
        """
        乘积最大子数组
        https://leetcode-cn.com/problems/maximum-product-subarray/
        当i+1位数为正，将前i个数的最大乘积放入数组d_max[i]
        当i+1位数为负，将前i个数的最小乘积放入数组d_min[i]
        """
        if not nums:
            return 0
        length = len(nums)
        if length == 1:
            return nums[0]
        d_max, d_min = [0] * length, [0] * length
        d_max[0] = d_min[0] = nums[0]
        for i, val in enumerate(nums[1:]):
            if val > 0:
                d_max[i + 1] = max(d_max[i] * val, val)
                d_min[i + 1] = min(d_min[i] * val, val)
            else:
                d_max[i + 1] = max(d_min[i] * val, val)
                d_min[i + 1] = min(d_max[i] * val, val)
        return max(d_max)

    def maxProfit(self, prices) -> int:
        # https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/
        min_val = prices[0]
        max_profit = 0
        for i in prices[1:]:
            max_profit = max(max_profit, i - min_val)
            min_val = min(min_val, i)
        return max_profit

    def lengthOfLIS(self, nums: List[int]) -> int:
        # 最长上升子序列 https://leetcode-cn.com/problems/longest-increasing-subsequence/submissions/
        if not nums:
            return 0
        d = [1] * len(nums)
        for i, val in enumerate(nums):
            for j in range(i + 1):
                if val > nums[j]:
                    d[i] = max(d[i], d[j] + 1)
        return max(d)


if __name__ == '__main__':
    s = Solution()

    res = s.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18])
    # res = s.findWords(
    #     board=[
    #         ['A', 'B', 'C', 'E'],
    #         ['S', 'F', 'C', 'S'],
    #         ['A', 'D', 'E', 'E']
    #     ], words=["ABCCED", "SEE", "ABCB"]
    # )
    # res = s.climbStairs(4)
    # res = s.minimumTotal([
    #     [2],
    #     [3, 4],
    #     [6, 5, 7],
    #     [4, 1, 8, 3]
    # ])
    print(res)
