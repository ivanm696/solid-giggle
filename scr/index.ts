import { WorkflowEntrypoint, WorkflowStep, WorkflowEvent } from 'cloudflare:workers';

// Настройки окружения (из твоего wrangler.toml)
type Env = {
  MY_WORKFLOW: Workflow;
  DOC_BUCKET: R2Bucket;
  MY_BROWSER: any;
};

type Params = {
  email: string;
  metadata: Record<string, string>;
};

// 1. КЛАСС WORKFLOW (Твоя новая логика)
export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    await step.do('log start', async () => {
      console.log("Workflow запущен для:", event.payload.email);
    });
    
    // Здесь можно добавить логику работы с R2 или Browser
  }
}

// 2. ОСНОВНОЙ ОБРАБОТЧИК (Твоя автоматизация + запуск Workflow)
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // --- ТВОЯ СУЩЕСТВУЮЩАЯ ЛОГИКА ДЛЯ BOT.TXT ---
    if (url.pathname === '/bot.txt') {
      return new Response("User-agent: *\nDisallow: /", {
        headers: { "Content-Type": "text/plain" }
      });
    }

    // --- ЗАПУСК НОВОГО WORKFLOW ---
    if (url.pathname === '/start-task') {
      const instance = await env.MY_WORKFLOW.create({
        params: { email: "admin@bot.com", metadata: { type: "auto" } }
      });
      return new Response(`Процесс запущен! ID: ${instance.id}`);
    }

    // Ответ по умолчанию
    return new Response("Система работает. Доступные пути: /bot.txt, /start-task");
  },
};
