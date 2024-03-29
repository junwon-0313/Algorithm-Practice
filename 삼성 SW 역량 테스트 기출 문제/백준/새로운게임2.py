# 체스판과 말 상태는 어떻게 관리할 것인가?
# 말을 순서대로 관리해야함. 왼쪽부터 아래에 있는 말입니다.
def main():
    # 출력 함수
    def print_chess():
        print("체스판 상태")
        for x in range(N):
            for y in range(N):
                print(graph[x][y], end=" ")
            print()

    # print_chess()
    def print_horse_pos():
        print("@@@@@말의 상태@@@@@")
        for x in range(N):
            for y in range(N):
                print(horse[x][y], end=" ")
            print()
        print("@@@@@@말의 방향@@@@@")
        print(horse_dir)
        print("@@@@@@말의 위치@@@@@")
        print(horse_pos)

    # 종료 조건: 4개 이상 쌓인 말이 있는지 체크
    def check_horse():
        for x in range(N):
            for y in range(N):
                if len(horse[x][y]) >= 4:
                    return True
        return False

    dir_lst = [0, (0, 1), (0, -1), (-1, 0), (1, 0)]
    N, K = map(int, input().split())
    # 체스판
    graph = []
    for _ in range(N):
        graph.append(list(map(int, input().split())))
    # 말의 위치를 그래프 위에 리스트로 관리
    horse = [[[] for _ in range(N)] for _ in range(N)]
    # 말의 방향
    horse_dir = [-1]
    # 말의 위치
    horse_pos = [(-1, -1)]

    # 초기 입력
    for idx in range(K):
        row, col, dir = map(int, input().split())
        row -= 1
        col -= 1
        horse[row][col].append((idx + 1))
        horse_dir.append(dir)
        horse_pos.append((row, col))
    # 종료 조건 global 변수
    global flag
    flag = False

    # 말의 이동: 1번 말부터~ K번째 말까지 이동
    def move_horse():
        global flag
        # 말의 위치를 사용 -> 이동, 말 위에 다른 말이 있는지 확인 있으면 같이 이동
        for horse_num in range(1, K + 1):
            pos = horse_pos[horse_num]
            for idx, num in enumerate(horse[pos[0]][pos[1]]):
                # 움직일 말을 기준으로 위에 있는 말은 모두 같이 이동
                if horse_num == num:
                    pivot_idx = idx
            # 왼쪽: 아래에 있는말, 남아있을 말 & 오른쪽: 이동할 말 분리
            horse[pos[0]][pos[1]], moving_horse = (
                horse[pos[0]][pos[1]][:pivot_idx],
                horse[pos[0]][pos[1]][pivot_idx:],
            )
            dir = horse_dir[horse_num]
            nx, ny = pos[0] + dir_lst[dir][0], pos[1] + dir_lst[dir][1]
            # nx, ny가 범위를 벗어날 때, 방향을 바꾸고 반대 방향으로 한칸
            if nx < 0 or nx > N - 1 or ny < 0 or ny > N - 1:
                if dir == 1:
                    horse_dir[horse_num] = 2
                elif dir == 2:
                    horse_dir[horse_num] = 1
                elif dir == 3:
                    horse_dir[horse_num] = 4
                elif dir == 4:
                    horse_dir[horse_num] = 3
                dir = horse_dir[horse_num]
                nx, ny = pos[0] + dir_lst[dir][0], pos[1] + dir_lst[dir][1]
                # 이동하려는 칸이 흰색인 경우
                if graph[nx][ny] == 0:
                    for num in moving_horse:
                        horse[nx][ny].append(num)
                        horse_pos[num] = (nx, ny)

                # 이동하려는 칸이 빨간색인 경우
                elif graph[nx][ny] == 1:
                    for num in moving_horse[::-1]:
                        horse[nx][ny].append(num)
                        horse_pos[num] = (nx, ny)

                # 이동하려는 칸이 파란색인 경우
                elif graph[nx][ny] == 2:
                    for num in moving_horse:
                        horse[pos[0]][pos[1]].append(num)
            # 벗어나지 않았을 때
            else:
                # 이동하려는 칸이 흰색인 경우
                if graph[nx][ny] == 0:
                    for num in moving_horse:
                        horse[nx][ny].append(num)
                        horse_pos[num] = (nx, ny)

                # 이동하려는 칸이 빨간색인 경우
                elif graph[nx][ny] == 1:
                    for num in moving_horse[::-1]:
                        horse[nx][ny].append(num)
                        horse_pos[num] = (nx, ny)

                # 이동하려는 칸이 파란색인 경우
                elif graph[nx][ny] == 2:
                    # 방향을 바꿔서 이동
                    if dir == 1:
                        horse_dir[horse_num] = 2
                    elif dir == 2:
                        horse_dir[horse_num] = 1
                    elif dir == 3:
                        horse_dir[horse_num] = 4
                    elif dir == 4:
                        horse_dir[horse_num] = 3
                    dir = horse_dir[horse_num]
                    nx, ny = pos[0] + dir_lst[dir][0], pos[1] + dir_lst[dir][1]
                    # 이동하려는 칸이 막힌 벗어날 경우
                    if nx < 0 or nx > N - 1 or ny < 0 or ny > N - 1:
                        for num in moving_horse:
                            horse[pos[0]][pos[1]].append(num)
                    # 이동하려는 칸이 흰색인 경우
                    elif graph[nx][ny] == 0:
                        for num in moving_horse:
                            horse[nx][ny].append(num)
                            horse_pos[num] = (nx, ny)
                    # 이동하려는 칸이 빨간색인 경우
                    elif graph[nx][ny] == 1:
                        for num in moving_horse[::-1]:
                            horse[nx][ny].append(num)
                            horse_pos[num] = (nx, ny)

                    # 이동하려는 칸이 파란색인 경우
                    elif graph[nx][ny] == 2:
                        for num in moving_horse:
                            horse[pos[0]][pos[1]].append(num)
            # print_horse_pos()
            # 언제든 말이 움직여서 4개이상이 되었을 때, 종료
            if check_horse():
                flag = True

    # 최대 1000번 반복
    for i in range(1, 1001):
        move_horse()
        if flag:
            print(i)
            return
    else:
        print(-1)


if __name__ == "__main__":
    main()
