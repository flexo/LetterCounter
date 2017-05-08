"""LetterCounter: Represent Base 26 as letters of the alphabet

Released under the MIT license:

Copyright (c) Nick Murdoch, 2006, 2007, 2010

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

ASCII_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class LetterIterator(object):
    """Iterates over letters A -> Z, AA -> AZ, BA -> BZ, etc."""
    def __init__(self, start='A', end=None, step=1, letters=ASCII_UPPERCASE):
        self.started = False
        self.current = start
        self.end = None
        if end:
            self.end = end
        self.step = step
        self.letters = letters

    def __iter__(self):
        return self
        
    def cycle_character(self, c):
        try:
            if c == self.letters[-1]:
                return self.letters[0]
            return self.letters[self.letters.index(c)+1]
        except ValueError as e:
            raise ValueError(str(e) + ": %c is not in %s" % (c, self.letters))

    def _next(self):
        # Edge cases:
        if self.current == self.end:
            raise StopIteration
        
        # Normal behaviour:
        for i in range(1, len(self.current)+2):
            if i <= len(self.current):
                self.current = self.current[:len(self.current)-i] \
                             + self.cycle_character(self.current[-i]) \
                             + self.current[len(self.current)-i+1:]
                if self.current[-i] != self.letters[0]:
                    # letter was not rolled back to A; we're done.
                    break
            else:
                # We've rolled back all the letters, need another column.
                self.current = self.letters[0] + self.current
        return self.current

    def __next__(self):
        # First iteration should return first number regardless of step
        if not self.started:
            self.started = True
            return self.current

        for i in range(self.step):
            next_ = self._next()
        return next_
    next = __next__
    

    def __cmp__(self, other):
        """Compare to another LetterIterator and return which is higher
        according to LetterIterator logic.
        
        The two LetterIterators must use the same letters string.
        """
        assert self.letters == other.letters
        if len(self.current) > len(other.current):
            return 1
        elif len(self.current) < len(other.current):
            return -1
        else:
            for pos in range(len(self.current)):
                index_self = self.letters.index(self.current[pos])
                index_other = other.letters.index(other.current[pos])
                if index_self > index_other:
                    return 1
                elif index_self < index_other:
                    return -1
                else:
                    continue
            else:
                return 0


class LetterCounter(object):
    """Letter Counter: Represent positive integers as letters
    A=0, B, C, ... Z, BA, BB, BC, ... 
        
    A is used as a 0, so AAAAAB is the same as B. For more common usage,
    use LetterIterator.
    """

    letters = ASCII_UPPERCASE
    base = 26

    def __init__(self, initial=""):
        self.value = initial
    
    def __repr__(self):
        return 'LetterCounter("'+self.unpad()+'")'
    
    def __str__(self):
        return self.value
    
    def __cmp__(self, other):
        # match lengths of self.value and other.value

        val1 = self.pad(max(len(self.value), len(other.value)))
        val2 = val2.pad(max(len(self.value), len(other.value)))

        if val1 < val2:
            return -1

        if val1 == val2:
            return 0

        if val1 > val2:
            return 1
    
    
    def __bool__(self):
        for c in self.value:
            if c != 'A':
                return True
        return False
    __nonzero__ = __bool__
    
    def __setattr__(self, name, value):
        if name == "value":
            object.__setattr__(self, name, value.upper())
    
    def __getattr__(self, name):
        if name == "value":
            return self.unpad()


    def __add__(self, other):
        return LetterCounter(self.from_int(int(self) + int(other)))
    
    def __sub__(self, other):
        return LetterCounter(self.from_int(int(self) - int(other)))
    
    def __mul__(self, other):
        return LetterCounter(self.from_int(int(self) * int(other)))
    
    def __div__(self, other):
        return LetterCounter(self.from_int(int(self) / int(other)))
    
    def __mod__(self, other):
        return LetterCounter(self.from_int(int(self) % int(other)))
    
    def __pow__(self, other):
        return LetterCounter(self.from_int(pow(int(self), int(other))))
    
    def __int__(self):
        ret = 0
        for v in reversed(range(len(self.value))):
            pos = len(self.value) - 1 - v
            ret += ( ord(self.value[pos]) - ord('A') ) * self.base**v
        return int(ret) # don't return Long if possible

    def from_int(cls, value):
        """Returns a string representing the integer provided.

        The string can be used to create a new LetterCounter or LetterIterator.
        """
        if value < 0:
            raise ValueError("value must be >= 0")
        i = 7
        s = ""
        while i >= 0:
            d = value//(cls.base**i)
            if d > 25:
                raise ValueError("value must be <= 208827064575")
            s += cls.letters[d]
            value = value - d*(cls.base**i)
            i -= 1
        return s
    from_int = classmethod(from_int)
    fromInt = from_int # backwards compat.

    def pad(self, padding):
        v = self.value
        while len(v) < padding:
            v = "A"+v
        return v
    
    def unpad(self):
        v = self.value
        while v.startswith('A'):
            v = v[1:]
        return v

