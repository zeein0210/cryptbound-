import random

# 카드 데이터 및 상성 정의
CARDS = {
    "나비": {"score": 10, "wins": "제비", "desc": "재사용 가능"},
    "두루미": {"score": 8, "wins": "사슴", "desc": "수명 변동 조절"},
    "제비": {"score": 6, "wins": "멧돼지", "desc": "상대 베팅 간파"},
    "사슴": {"score": 4, "wins": "나비", "desc": "중복 패 간파"},
    "멧돼지": {"score": 2, "wins": "두루미", "desc": "효과 무효화"}
}

def play_game():
    print("=== 수명 베팅 카드 게임 시뮬레이터 ===")
    
    # 1. 초기 설정
    try:
        num_players = int(input("참여할 플레이어 인원수를 입력하세요: "))
        start_life = int(input("모두의 초기 수명을 입력하세요: "))
    except:
        print("숫자로 입력해주세요."); return

    players = []
    for i in range(num_players):
        name = f"플레이어{i+1}"
        # 중복 상관없이 3장 무작위 배분
        hand = random.choices(list(CARDS.keys()), k=3)
        players.append({"name": name, "life": start_life, "hand": hand})

    print(f"\n--- 게임 시작 (모두 {start_life}년의 수명으로 시작합니다) ---")

    # 2. 라운드 진행 (1라운드 예시)
    for p in players:
        print(f"\n[{p['name']}의 턴] 현재 수명: {p['life']}년")
        print(f"보유 카드: {p['hand']}")
        p['pick'] = input(f"낼 카드를 입력하세요: ")
        p['bet'] = int(input(f"베팅할 수명을 입력하세요: "))

    # 3. 능력 및 점수 계산
    # 멧돼지 무효화 체크
    boar_active = any(p['pick'] == "멧돼지" for p in players)
    
    results = []
    total_bet_pool = 0

    for p in players:
        base_score = CARDS[p['pick']]['score']
        bet_score = p['bet']
        matchup_bonus = 0
        total_bet_pool += p['bet']

        # 상성 계산 (멧돼지 효과가 없을 때만)
        if not boar_active:
            for opp in players:
                if p == opp: continue
                if CARDS[p['pick']]['wins'] == opp['pick']:
                    matchup_bonus += 3
                elif CARDS[opp['pick']]['wins'] == p['pick']:
                    matchup_bonus -= 1
        
        total_score = base_score + bet_score + matchup_bonus
        results.append({"player": p, "score": total_score})

    # 4. 승자 판정
    if boar_active:
        print("\n⚠️ 멧돼지 발동! 모든 상성과 특수 능력이 무효화되었습니다.")

    winner_entry = max(results, key=lambda x: x['score'])
    winner = winner_entry['player']
    
    print(f"\n🏆 라운드 승리자: {winner['name']} (총점: {winner_entry['score']})")

    # 5. 수명 정산 (두루미 능력 반영)
    for p in players:
        if p == winner:
            gain = total_bet_pool
            if p['pick'] == "두루미" and not boar_active:
                gain *= 2
                print(f"✨ 두루미 효과! 승리 보상이 2배가 됩니다 (+{gain})")
            p['life'] += gain
        else:
            loss = p['bet']
            if p['pick'] == "두루미" and not boar_active:
                loss //= 2
                print(f"🛡️ 두루미 효과! 패배 손실이 절반으로 줄어듭니다 (-{loss})")
            p['life'] -= loss
        
        print(f"{p['name']}의 남은 수명: {p['life']}년")

if __name__ == "__main__":
    play_game()