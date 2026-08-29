# What I checked, and what the agent got wrong

Write this yourself, in your own words. It is the part of the repo that proves the work is yours.

## What the agent got wrong
When I asked my agent to add the missing test for the no reading crash, it
didn't add it alongside the existing tests, it replaced the whole file,
wiping out the import statement, the SAMPLE fleet data, and the original
due car test along with it. I caught it because verify.py told me the test
file only had 1 test when it should have had 2. I went back into the file,
saw the original test was gone, and put it back alongside the new one.

## What I checked before I accepted its work
I ran pytest until every test passed, then ran python verify.py and went
through all 11 checks until every line read PASS. That included confirming
the wear calculation reads about 99.3% for a nearly-worn car instead of 0%,
the average wear reads about 59.67%, and the km-to-miles conversion reads
about 62.1 miles per 100 km. I specifically checked that SERVICE_INTERVAL_KM,
WARN_AT_PERCENT, and the values in settings.cfg were still 15000 km and 80%
those weren't supposed to change, and verify.py confirmed they hadn't.

## What the data actually said
The data showed that the main factors linked to breakdowns were how long it had been since the last service, the average kilometres driven per day, and the load on the car. Surprisingly, total kilometres on the odometer didn't really make much difference. The age of the car also didn't show any meaningful difference between cars that broke down and those that didn't. So, in this dataset, recent usage and maintenance seemed to matter more than the car's overall age or mileage.
