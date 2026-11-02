const assert=require('node:assert/strict'),C=require('../public/core.js');
for(const [date,minutes] of [['2026-11-02T22:30:00Z',90],['2026-07-01T22:59:30Z',1],['2026-03-29T00:00:00Z',1380],['2026-10-24T23:00:00Z',1500]])assert.equal(C.minutesToNextDay(new Date(date)),minutes);
console.log('PASS Lisbon countdown winter, summer, minute rounding and both DST transitions');
