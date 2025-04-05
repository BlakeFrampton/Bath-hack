from PySide6.QtGui import (QBrush, QColor, QFont, QKeyEvent,
                           QMouseEvent, QTextCharFormat, Qt)
from PySide6.QtWidgets import QApplication, QTextEdit
import textGenerator
import sys
import os
from dotenv import load_dotenv


class TypingBox(QTextEdit):

    def __init__(self, **_):
        super().__init__()

        load_dotenv()
        self.setFont(QFont("Times", 18, QFont.Bold))
        self.streak = 0
        self.mistakes = 0
        self.correct = 0
        # textToType = self.getText()
        # self.setTextToType(textToType)
        self.setFont(QFont("Times", 50, QFont.Bold))
        self.setTextToType("""TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
TestTestTestTestTestTestTestTestTestTest
        """)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setOverwriteMode(True)
        self.mistakesOverride = False

    def reset(self):
        self.streak = 0
        self.mistakes = 0
        self.correct = 0

        # remove the current text
        format = QTextCharFormat()
        format.setForeground(QBrush(QColor("black")))
        cursor = self.textCursor()
        while cursor.position() > 0:
            self.backspace(cursor, cursor.position(), format, "")


    def keyPressEvent(self, e: QKeyEvent) -> None:
        cursor = self.textCursor()
        pos = cursor.position()
        format = QTextCharFormat()

        print("streak: ", self.streak)
        try:
            if e.text() == self._textToType[pos]:
                format.setForeground(QBrush(QColor("green")))
                cursor.deleteChar()
                cursor.setCharFormat(format)
                cursor.insertText(e.text())
                cursor.setPosition(pos + 1)
                pos += 1
                self.correct += 1
                self.streak += 1
            elif ord(e.text()) == 8:  # Backspace
                if pos > 0:
                    self.backspace(cursor, pos, format, e)
            elif ord(e.text()) == 127:  # Ctrl-backspace
                startingSpace = False
                if self._textToType[pos - 1] == " ":  # If pressed while on a space
                    # delete from space to start of previous word
                    startingSpace = True
                while startingSpace or (pos > 0 and self._textToType[pos - 1] != " "):
                    # Backspace until start of text or word
                    startingSpace = False
                    self.backspace(cursor, pos, format, e)
                    pos = cursor.position()
            else:
                self.mistakes += 1
                self.streak = 0
                format.setForeground(QBrush(QColor("red")))
                cursor.deleteChar()
                cursor.setCharFormat(format)
                cursor.insertText(self._textToType[pos])
                cursor.setPosition(pos + 1)
                pos += 1
        except TypeError:
            pass

        if pos == len(self._textToType):
            cursor.setPosition(0)  # Loop Back
            self.setTextCursor(cursor)
            finishedTest(self.toPlainText(), self._textToType, self.correct, self.mistakes)
            self.streak = 0
            self.correct = 0
            self.mistakes = 0

    def backspace(self, cursor, pos, format, e):
        indx = (pos - 1) % len(self._textToType)
        print(indx)
        cursor.setPosition(indx)
        cursor.deleteChar()
        cursor.setCharFormat(format)
        if self.mistakesOverride:
            cursor.insertText(e.text())
        else:
            cursor.insertText(self._textToType[indx])
        cursor.setPosition(indx)
        self.setTextCursor(cursor)

    def insertFromMimeData(self, _) -> None:
        pass  # Disable Pasting

    def textToType(self) -> str:
        return self.toPlainText()

    def setTextToType(self, message: str) -> None:
        self._textToType = message
        return self.setText(message)

    def getText(self):
        targetLength = 200
        notes = """We need persistent storage to maintain data between processing steps, hard disks/SSDs provide this.

Their underlying structure is a set of blocks.

A block can only be read or written in its entirety.

![image.png](attachment:dc6632a5-9b89-44db-b2e3-4001571477f3:image.png)

Storing data in blocks is not very intuitive for programmers so we abstract this away using files.

Files at their simplest allow opening, reading or writing in sequence, and closing.

Modern systems also allow us to seek to any point in the file.

**File Types**

Files are named objects and the convention is that the characters after the last ‘.’ indicates their file type.

In Linux this is just convention, but in Windows the OS makes use of this.

**Directories**

Files usually exist in a directory or folder hierarchy. We can separate system and user files.

This also helps with security, as we can apply permissions to directories, as well as files.

Files have a range of additional attributes (meta-data). Their purpose is similar to the status bits in a page table.

![image.png](attachment:807d38c0-b5d2-4eb2-8039-12a35fbfbb42:image.png)

**File Management**

We could allocate storage in much the same way we did when using segments (know the size of the file, find a space in storage large enough to hold it), but this would have all the same problems we saw with memory. 

**Linked lists** are a potential alternative.

The first few bytes in a block will tell us where the next block in the file is located. This allows for variable sized files, with minimal wasted space.

But it means the blocks which are a power of two would hold a non-power of two data block. As memory is dealt with in power of two blocks, this creates a mismatch that will complicate things.

![image.png](attachment:8b62d678-5400-4425-9f89-2ba442a520d9:image.png)

Another alternative is a **File Allocation Table (FAT)**

Instead of holding the list inside the blocks, we allocate specific storage to it.

Each entry in the table tells us which block is next for a file and in that table address we hold the next entry.

We will need a marker to tell us when to stop.

We’ll want to keep the whole table in memory for speed of access.

![image.png](attachment:9d13ba0e-5687-4567-a3fe-c333256009eb:image.png)

To avoid loading the whole table, we can use i**-nodes** instead

Each i-node has an array of indexes to disk blocks

The last index can be the index of a block that contains further indices.

This is more efficient as we only need to load the i-nodes of the files that are open.

![image.png](attachment:39a7eb30-d24a-491d-974f-3e2cbaab1df1:image.png)

**Directory Implementation**

Each file needs a name, location, and attributes. Directories need something similar.

A directory is just a file that lists the files it contains.

Each file record will hold a name and a reference to the first storage location

**Shared Files**

Often, we want multiple processes to access a file.

Sometimes, it’s helpful to reference a file from a different path.

i-nodes give us the option to do this, we can have the directory give a link to the i-node.

Having a file in more than one directory is known as **linking**.

- Hard-links: share the control object of a file e.g. i-node
- Soft-links: just hold the whole filename of the linked to file and the system must follow the path (i.e. a shortcut)

**Logs and Journaling**

As disks get bigger, the access patterns change, we end up with more, smaller writes.

One solution is to record a log of changes and write these as combined operations.

We then need a helper process to remove old information and compact it to keep storage efficient.

We can extend the idea of a log to make the file system more robust

The log allows us to reconstruct the state of the file system at the time of failure.

For this to work, we need the log operations to be repeatable without any corruption being caused. This is known as **idempotent**

We can also make all log operations **atomic**. This means they either happen in their entirety or not at all.

**SSD**

Flash memory based devices with no moving parts. SSD pages can’t just be overwritten, they need to be erased first.

To compensate for files that keep being updated, a wear-levelling algorithm is used. This avoids re-using the same page over and over.

The file system block size and the flash page size may not be the same.

**Virtual File Systems**

We put a virtual file system layer between the user access to files and the individual filesystems supported by an OS so we don’t limit ourselves to just one type of file system per operating system.

Backups are also known as **dumps** of the data

If we copy the entire raw device partition to our backup medium, it is called a **physical dump**

It is smarter to backup at the logical level, independent of the particular filesystem format

This is known as a **logical dump**.

We can use attributes in a file to know when it was last backed up and only copy what has changed since. This is an **incremental dump.**

It’s not unusual for us to have more than one copy of some data on our filesystem e.g. a common file in the home directory of every user, or a saved copy of a previous version of software you are developing

**Deduplication** is the process of spotting the replication and sharing the data instead.

**Security**

Even if the OS enforces access restrictions on users, how do we prevent someone accessing data if they take the disk out of the machine?

Some applications offer the ability to password encrypt individual files.

It’s also possible to implement disk-based encryption, blocks will be encrypted/decrypted as they are copied between memory and the device

The whole device encryption requires a password to be entered on start-up of device"""
        difficultWords = ["cappuccino", "spring", "crisp", "establishment"]
        return getTextToType(theme, difficultWords, targetLength,
                             True, os.environ.get("OPENAI_API_KEY"))


def finishedTest(typed: str, target: str, correct: int, mistakes: int):
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingBox()
    window.show()
    sys.exit(app.exec())
