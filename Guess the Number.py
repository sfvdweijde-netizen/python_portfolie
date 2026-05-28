import random
import os

HIGH_SCORE_FILE = "highscore.txt"


def get_high_score() -> int:
    """Reads the current high score from a file. Returns 999 if no high score exists."""
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 999
    return 999


def save_high_score(score: int):
    """Saves a new high score to the file."""
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


def choose_difficulty() -> int:
    """Prompts the player to choose a difficulty level and returns the max attempts."""
    print("Select Difficulty Level:")
    print("1. Easy   (Unlimited attempts)")
    print("2. Medium (10 attempts)")
    print("3. Hard   (5 attempts)")

    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            return float('inf')  # Infinity
        elif choice == "2":
            return 10
        elif choice == "3":
            return 5
        print("❌ Invalid choice. Please enter 1, 2, or 3.")


def play_guess_the_number():
    print("====================================")
    print("Welcome to the Number Guessing Game!")
    print("====================================")

    current_high_score = get_high_score()
    if current_high_score != 999:
        print(f"🏆 Current High Score (Fewest Attempts): {current_high_score}\n")
    else:
        print("🏆 No high score recorded yet. Be the first!\n")

    max_attempts = choose_difficulty()
    secret_number = random.randint(1, 100)
    attempts = 0
    guessed_correctly = False

    print("\nI have chosen a number between 1 and 100. Start guessing!")

    while not guessed_correctly and attempts < max_attempts:
        # Show remaining attempts for medium and hard mode
        if max_attempts != float('inf'):
            print(f"Attempts remaining: {max_attempts - attempts}")

        user_input = input("Enter your guess: ")

        try:
            guess = int(user_input)
        except ValueError:
            print("❌ Invalid input! Please enter a valid whole number.\n")
            continue

        attempts += 1

        if guess < 1 or guess > 100:
            print("⚠ Out of bounds! Guess between 1 and 100.\n")
        elif guess < secret_number:
            print("📈 Too low!\n")
        elif guess > secret_number:
            print("📉 Too high!\n")
        else:
            guessed_correctly = True
            print(f"\n🎉 Congratulations! You guessed the number {secret_number}!")
            print(f"🏅 Total attempts: {attempts}")

            # Check for a new high score
            if attempts < current_high_score:
                print("🔥 NEW HIGH SCORE! 🔥")
                save_high_score(attempts)

    if not guessed_correctly:
        print(f"\n💥 Game Over! You ran out of attempts. The number was {secret_number}.")


if __name__ == "__main__":
    play_guess_the_number()
