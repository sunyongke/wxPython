###############################################################################
# Name: asm.py                                                                #
# Purpose: Define ASM syntax for highlighting and other features              #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2007 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: asm.py
AUTHOR: Cody Precord
@summary: Lexer configuration file GNU Assembly Code
@todo: Complete Keywords/Registers

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import wx.stc as stc

# Local Imports
import synglob
import syndata
#-----------------------------------------------------------------------------#

# GNU Assembly CPU Instructions/Storage Types
ASM_CPU_INST = (0, ".long .ascii .asciz .byte .double .float .hword .int .octa "
                   ".quad .short .single .space .string .word")

# GNU FPU Instructions
ASM_MATH_INST = (1, "")

# GNU Registers
ASM_REGISTER = (2, "")

# GNU Assembly Directives/Special statements/Macros
ASM_DIRECTIVES = (3, ".include .macro .endm")

#---- Language Styling Specs ----#
SYNTAX_ITEMS = [ ('STC_ASM_DEFAULT', 'default_style'),
                 ('STC_ASM_CHARACTER', 'char_style'),
                 ('STC_ASM_COMMENT', 'comment_style'),
                 ('STC_ASM_COMMENTBLOCK', 'comment_style'),
                 ('STC_ASM_CPUINSTRUCTION', 'keyword_style'),
                 ('STC_ASM_DIRECTIVE', 'keyword3_style'),
                 ('STC_ASM_DIRECTIVEOPERAND', 'default_style'),
                 ('STC_ASM_EXTINSTRUCTION', 'default_style'),
                 ('STC_ASM_IDENTIFIER', 'default_style'),
                 ('STC_ASM_MATHINSTRUCTION', 'keyword_style'),
                 ('STC_ASM_NUMBER', 'number_style'),
                 ('STC_ASM_OPERATOR', 'operator_style'),
                 ('STC_ASM_REGISTER', 'keyword2_style'),
                 ('STC_ASM_STRING', 'string_style'),
                 ('STC_ASM_STRINGEOL', 'stringeol_style') ]

#-----------------------------------------------------------------------------#

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Assembly files""" 
    def __init__(self, langid):
        syndata.SyntaxDataBase.__init__(self, langid)

        # Setup
        # synglob.ID_LANG_ASM
        self.SetLexer(stc.STC_LEX_ASM)

    def Keywords(self):
        """Returns List of Keyword Specifications
        @param lang_id: used to select specific subset of keywords

        """
        return [ASM_CPU_INST, ASM_DIRECTIVES]

    def SyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [u';']
