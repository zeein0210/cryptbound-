import random

CARDS = {
    "나비": {"score": 10, "wins": "제비"},
    "두루미": {"score": 8, "wins": "사슴"},
    "제비": {"score": 6, "wins": "멧돼지"},
    "사슴": {"score": 4, "wins": "나비"},
    "멧돼지": {"score": 2, "wins": "두루미"}
}

def run_game():
    print("=== 수명 베팅 게임 'ANIMA' (3라운드 모드) ===")
    num_players = int(input("인원수: "))
    start_life = int(input("초기 수명: "))
    
    # 플레이어 초기화
    players = []
    for i in range(num_players):
        # 3라운드를 위해 미리 3장 배분
        hand = random.choices(list(CARDS.keys()), k=3)
        players.append({"name": f"P{i+1}", "life": start_life, "hand": hand, "last_card": None})

    # 3라운드 반복
    for r_num in range(1, 4):
        print(f"\n" + "="*30)
        print(f"      ROUND {r_num} START")
        print("="*30)
        
        round_data = []
        for p in players:
            print(f"\n{p['name']}의 현재 수명: {p['life']}")
            print(f"{p['name']}의 남은 패: {p['hand']}")
            
            # 나비 능력: 이전 카드 재사용 안내
            if p['last_card']:
                print(f"(나비 능력 사용 가능: 이전 카드 '{p['last_card']}' 재사용 가능)")

            pick = input(f"{p['name']} 선택 카드: ")
            bet = int(input(f"{p['name']} 베팅 수명: "))
            
            # 패에서 제거 (재사용 능력이 아닐 경우에만 실제 제거 로직은 복잡하므로 여기선 기본 차감)
            if pick in p['hand']:
                p['hand'].remove(pick)
            
            p['last_card'] = pick
            round_data.append({"p": p, "pick": pick, "bet": bet})

        # 계산 로직
        boar_active = any(d['pick'] == "멧돼지" for d in round_data)
        total_bet_pool = sum(d['bet'] for d in round_data)
        results = []

        for d in round_data:
            score = CARDS[d['pick']]['score'] + d['bet']
            if not boar_active:
                for opp in round_data:
                    if d == opp: continue
                    if CARDS[d['pick']]['wins'] == opp['pick']: score += 3
                    elif CARDS[opp['pick']]['wins'] == d['pick']: score -= 1
            results.append({"data": d, "total_score": score})

        # 라운드 승자 정산
        winner_res = max(results, key=lambda x: x['total_score'])
        winner = winner_res['data']['p']
        print(f"\n▶ 라운드 {r_num} 승자: {winner['name']}!")

        for r in results:
            p_data = r['data']
            player = p_data['p']
            if player == winner:
                gain = total_bet_pool
                if p_data['pick'] == "두루미" and not boar_active: gain *= 2
                player['life'] += gain
            else:
                loss = p_data['bet']
                if p_data['pick'] == "두루미" and not boar_active: loss //= 2
                player['life'] -= loss
            
            if player['life'] <= 0:
                print(f"💀 {player['name']}의 수명이 다했습니다!")

    print("\n" + "!"*30)
    print("      최종 게임 종료")
    for p in players:
        print(f"{p['name']}: 최종 수명 {p['life']}년")
    print("!"*30)

if __name__ == "__main__":
    run_game()
