const OWNER = "alonmorad9";
const REPO = "real-stock-alert";
const WORKFLOW = "main.yml";

function modeForSchedule(schedule, now) {
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
