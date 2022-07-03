import os
from datetime import date
from imapclient import IMAPClient


class ImapClient:
    def __init__(self, server, username, password, cleanup=False) -> None:
        self.server = IMAPClient(server, use_uid=True, ssl=True)
        self.current_folder = "/"
        self.server_dir = self.__prepare_serverfolder(username)
        self.with_cleanup = cleanup
        self.server.login(username, password)

    def __prepare_serverfolder(self, email):
        outdir = f'{email.replace("@", "_")}'
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        return outdir

    def __retrieve_mails(self):
        messages = self.server.search("ALL")
        for msgid, data in self.server.fetch(messages, ["RFC822"]).items():
            data = data.get(b"RFC822")

            outdir = os.path.join(self.server_dir, self.current_folder)
            if not os.path.exists(outdir):
                os.makedirs(outdir)

            outpath = os.path.join(outdir, f"{msgid}.eml")
            out = open(outpath, "wb")
            out.write(data)
            out.close
        if self.with_cleanup:
            self.server.delete_messages(messages=messages)

    def process_folders(self):
        folders = self.server.list_folders()
        for f in folders:
            self.current_folder = f[-1]
            try:
                sel = self.server.select_folder(self.current_folder)
            except Exception as e:
                print(f"Error read folder {self.current_folder}: {e}")
                continue

            count_mail = sel[b"EXISTS"]
            print(f"{count_mail} messages in {self.current_folder}")
            if count_mail != 0:
                self.__retrieve_mails()

        return


if __name__ == "__main__":
    client = ImapClient("imap.<server>", "<email>", "password", cleanup=False)
    client.process_folders()
