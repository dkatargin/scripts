import os

def main():
    target_dir = "/home/dmitry/Desktop/meru-emotes-emojigg-pack/"
    for filename in os.listdir(target_dir):
        new_name = "_".join(filename.split("-")[1:])
        os.rename(os.path.join(target_dir, filename), os.path.join(target_dir, new_name))
if __name__ == "__main__":
    main()
