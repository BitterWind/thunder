leaderboard = [('3', 55.0), ('8', 35.0), ('6', 29.0), ('9', 16.0), ('4', 11.0), ('2', 9.0), ('7', 7.0), ('5', 0.0), ('1', 0.0)]
ans = {}
for rank,(id, score) in enumerate(leaderboard):
    print(score)
    ans[str(rank)] = (id, score)
    rank+=1
print(ans)