const OWNER = "alonmorad9";
const REPO = "real-stock-alert";
const WORKFLOW = "main.yml";

function dateFromUTC(now) {
  return new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
}

function addDays(date, days) {
  const next = new Date(date);
  next.setUTCDate(next.getUTCDate() + days);
  return next;
}

function observedFixedHoliday(year, monthIndex, day) {
  const holiday = new Date(Date.UTC(year, monthIndex, day));
  if (holiday.getUTCDay() === 6) return addDays(holiday, -1);
  if (holiday.getUTCDay() === 0) return addDays(holiday, 1);
  return holiday;
}

function nthWeekday(year, monthIndex, weekday, n) {
  let day = new Date(Date.UTC(year, monthIndex, 1));
  while (day.getUTCDay() !== weekday) {
    day = addDays(day, 1);
  }
  return addDays(day, 7 * (n - 1));
}

function lastWeekday(year, monthIndex, weekday) {
  let day = new Date(Date.UTC(year, monthIndex + 1, 0));
  while (day.getUTCDay() !== weekday) {
    day = addDays(day, -1);
  }
  return day;
}

function easterDate(year) {
  const a = year % 19;
  const b = Math.floor(year / 100);
  const c = year % 100;
  const d = Math.floor(b / 4);
  const e = b % 4;
  const f = Math.floor((b + 8) / 25);
  const g = Math.floor((b - f + 1) / 3);
  const h = (19 * a + b - d - g + 15) % 30;
  const i = Math.floor(c / 4);
  const k = c % 4;
  const l = (32 + 2 * e + 2 * i - h - k) % 7;
  const m = Math.floor((a + 11 * h + 22 * l) / 451);
  const month = Math.floor((h + l - 7 * m + 114) / 31);
  const day = ((h + l - 7 * m + 114) % 31) + 1;
  return new Date(Date.UTC(year, month - 1, day));
}

function isoDate(date) {
  return date.toISOString().slice(0, 10);
}

function marketHolidays(year) {
  return new Set([
    isoDate(observedFixedHoliday(year, 0, 1)),
    isoDate(nthWeekday(year, 0, 1, 3)),
    isoDate(nthWeekday(year, 1, 1, 3)),
    isoDate(addDays(easterDate(year), -2)),
    isoDate(lastWeekday(year, 4, 1)),
    isoDate(observedFixedHoliday(year, 5, 19)),
    isoDate(observedFixedHoliday(year, 6, 4)),
    isoDate(nthWeekday(year, 8, 1, 1)),
    isoDate(nthWeekday(year, 10, 4, 4)),
    isoDate(observedFixedHoliday(year, 11, 25)),
    isoDate(observedFixedHoliday(year + 1, 0, 1)),
  ]);
}

function isMarketTradingDay(now) {
  const tradingDay = dateFromUTC(now);
  const weekday = tradingDay.getUTCDay();
  if (weekday === 0 || weekday === 6) return false;
  return !marketHolidays(tradingDay.getUTCFullYear()).has(isoDate(tradingDay));
}

function modeForSchedule(schedule, now) {
  if (!isMarketTradingDay(now)) {
    return null;
  }
  if (now.getUTCHours() === 13 && now.getUTCMinutes() === 45) {
    return "opening";
  }
  if (!(now.getUTCHours() === 21 && now.getUTCMinutes() === 30)) {
    return null;
  }
  const day = now.getUTCDay();
  return day === 5 ? "weekly" : "daily";
}

async function dispatchWorkflow(env, mode) {
  const response = await fetch(
    `https://api.github.com/repos/${OWNER}/${REPO}/actions/workflows/${WORKFLOW}/dispatches`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.GITHUB_TOKEN}`,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "real-stock-alert-scheduler",
      },
      body: JSON.stringify({
        ref: "main",
        inputs: { mode },
      }),
    },
  );

  if (!response.ok) {
    throw new Error(`GitHub dispatch failed: ${response.status} ${await response.text()}`);
  }
}

export default {
  async scheduled(event, env, ctx) {
    const now = new Date(event.scheduledTime);
    const mode = modeForSchedule(event.cron, now);
    if (!mode) {
      return;
    }
    ctx.waitUntil(dispatchWorkflow(env, mode));
  },

  async fetch(request, env) {
    const url = new URL(request.url);
    const mode = url.searchParams.get("mode") || modeForSchedule("", new Date());
    if (!["daily", "weekly", "opening", "manual"].includes(mode)) {
      return new Response("Invalid mode", { status: 400 });
    }
    await dispatchWorkflow(env, mode);
    return new Response(`Dispatched ${mode}\n`);
  },
};
