import random

# 카드 데이터: 점수 및 상성(승리대상)
CARDS = {
    "나비": {"score": 10, "wins": "제비"},
    "두루미": {"score": 8, "wins": "사슴"},
    "제비": {"score": 6, "wins": "멧돼지"},
    "사슴": {"score": 4, "wins": "나비"},
    "멧돼지": {"score": 2, "wins": "두루미"}
}

def run_game():
    # 1. 초기 데이터 입력
    num_players = int(input("인원수: "))
    start_life = int(input("초기 수명: "))
    
    players = []
    for i in range(num_players):
        # 중복 허용 무작위 3장 배분
        hand = random.choices(list(CARDS.keys()), k=3)
        players.append({"name": f"P{i+1}", "life": start_life, "hand": hand})

    # 2. 각 플레이어 카드 및 베팅액 입력
    round_data = []
    for p in players:
        print(f"\n{p['name']}의 패: {p['hand']}")
        pick = input(f"{p['name']} 선택 카드: ")
        bet = int(input(f"{p['name']} 베팅 수명: "))
        round_data.append({"p": p, "pick": pick, "bet": bet})

    # 3. 자동 계산 엔진
    boar_active = any(d['pick'] == "멧돼지" for d in round_data)
    total_bet_pool = sum(d['bet'] for d in round_data)
    results = []

    for d in round_data:
        # 총합 = 패 등급 점수 + 수명 베팅 + 상성 보너스
        score = CARDS[d['pick']]['score'] + d['bet']
        
        # 상성 보너스 (+3, -1) - 멧돼지 없을 때만 작동
        if not boar_active:
            for opp in round_data:
                if d == opp: continue
                if CARDS[d['pick']]['wins'] == opp['pick']:
                    score += 3
                elif CARDS[opp['pick']]['wins'] == d['pick']:
                    score -= 1
        
        results.append({"data": d, "total_score": score})

    # 4. 승자 판정 및 수명 정산
    winner_res = max(results, key=lambda x: x['total_score'])
    winner = winner_res['data']['p']

    print(f"\n결과: {winner_res['data']['p']['name']} 승리 (총점: {winner_res['total_score']})")
    if boar_active: print("(멧돼지 효과로 상성/능력 무효화됨)")

    for r in results:
        p_data = r['data']
        player = p_data['p']
        
        if player == winner:
            gain = total_bet_pool
            # 두루미 승리 시 2배
            if p_data['pick'] == "두루미" and not boar_active: gain *= 2
            player['life'] += gain
        else:
            loss = p_data['bet']
            # 두루미 패배 시 절반
            if p_data['pick'] == "두루미" and not boar_active: loss //= 2
            player['life'] -= loss
        
        print(f"{player['name']} 최종 수명: {player['life']}")

if __name__ == "__main__":
    run_game()명: {p['life']}년")

if __name__ == "__main__":
    play_game()
