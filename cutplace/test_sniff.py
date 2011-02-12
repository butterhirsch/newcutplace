"""
Test for `sniff` module.
"""
# Copyright (C) 2009-2010 Thomas Aglassinger
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import unittest
import StringIO

import data
import sniff
import dev_test

class SniffTest(unittest.TestCase):

    def testCreateDataFormat(self):
        fileNameToExpectedFormatMap = {
            "valid_customers.csv": data.FORMAT_DELIMITED,
            "valid_customers.ods": data.FORMAT_ODS,
            "valid_customers.xls": data.FORMAT_EXCEL,
        }
        for testFileName, exptectedDataFormatName in fileNameToExpectedFormatMap.items():
            testFilePath = dev_test.getTestInputPath(testFileName)
            testFile = open(testFilePath, "rb")
            try:
                actualDataFormat = sniff.createDataFormat(testFile)
                actualDataFormatName = actualDataFormat.name
                self.assertEqual(actualDataFormatName, exptectedDataFormatName,
                    "data format for file must be %r but is %r: %r" % (exptectedDataFormatName, actualDataFormatName, testFilePath))
            finally:
                testFile.close()

    def testDelimitedOptions(self):
        fileNameToExpectedOptionsMap = {
            "valid_customers.csv": {
                sniff._ITEM_DELIMITER: ",",
                sniff._ESCAPE_CHARACTER: "\"",
                sniff._ENCODING: 'ascii',
                sniff._QUOTE_CHARACTER: "\""
            },
        }
        for testFileName, exptectedDelimitedOptions in fileNameToExpectedOptionsMap.items():
            testFilePath = dev_test.getTestInputPath(testFileName)
            testFile = open(testFilePath, "rb")
            try:
                actualDelimitedOptions = sniff.delimitedOptions(testFile)

                # Add actual line delimiter as expected. We cannot provide a proper expected line
                # delimiter in ``exptectedDelimitedOptions`` because the actual value depend on
                # the platform the repository has been checked out to. 
                actualLineDelimiter = actualDelimitedOptions["lineDelimiter"]
                self.assertTrue(actualLineDelimiter)
                exptectedDelimitedOptions["lineDelimiter"] = actualLineDelimiter

                self.assertEqual(actualDelimitedOptions, exptectedDelimitedOptions, \
                    "data format for file must be %r but is %r: %r" % (exptectedDelimitedOptions, actualDelimitedOptions, testFilePath))
            finally:
                testFile.close()

    def testCreateReader(self):
        testFileNames = [
            "valid_customers.csv",
            "valid_customers.ods",
            "valid_customers.xls"
        ]
        for testFileName in testFileNames:
            testFilePath = dev_test.getTestInputPath(testFileName)
            testFile = open(testFilePath, "rb")
            try:
                reader = sniff.createReader(testFile)
                rowCount = 0
                for _ in reader:
                    rowCount += 1
                self.assertTrue(rowCount > 0)
            finally:
                testFile.close()
        
    def testEmpty(self):
        emptyReadable = StringIO.StringIO("")

        self.assertTrue(sniff.delimitedOptions(emptyReadable))

        emptyDataFormat = sniff.createDataFormat(emptyReadable)
        self.assertTrue(emptyDataFormat)
        self.assertEqual(emptyDataFormat.name, data.FORMAT_DELIMITED)

        emptyReader = sniff.createReader(emptyReadable)
        self.assertTrue(emptyReadable)
        rowCount = 0
        for _ in emptyReader:
            rowCount += 1
        self.assertEqual(rowCount, 0)
        
    def testCreateEmptyInterfaceControlDocument(self):
        emptyReadable = StringIO.StringIO("")
        self.assertRaises(sniff.CutplaceSniffError, sniff.createInterfaceControlDocument, emptyReadable)

    def testCreateInterfaceControlDocument(self):
        testFileNames = [
            "valid_customers.csv",
            "valid_customers.ods",
            "valid_customers.xls"
        ]
        for testFileName in testFileNames:
            testFilePath = dev_test.getTestInputPath(testFileName)
            testFile = open(testFilePath, "rb")
            try:
                # TODO: Add assertions to actually test instead of just exercise.
                sniff.createInterfaceControlDocument(testFile)
            finally:
                testFile.close()

    def testHeaderAndStopAfter(self):
        testFileNames = [
            "valid_customers.csv",
            "valid_customers.ods",
            "valid_customers.xls"
        ]
        for testFileName in testFileNames:
            testFilePath = dev_test.getTestInputPath(testFileName)
            testFile = open(testFilePath, "rb")
            try:
                reader = sniff.createReader(testFile)
                rowCount = 0
                for _ in reader:
                    rowCount += 1
                self.assertTrue(rowCount > 0)
            finally:
                testFile.close()
        
if __name__ == "__main__":
    import logging
    logging.basicConfig()
    logging.getLogger("cutplace").setLevel(logging.DEBUG)
    unittest.main()