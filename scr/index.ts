import { WorkflowEntrypoint, WorkflowStep, WorkflowEvent } from 'cloudflare:workers';

// Определяем типы для окружения
export interface Env {
  MY_WORKFLOW: Workflow;
}

// Параметры, которые мы передаем боту
type Params = {
  email: string;
  metadata: Record<string, string>;
};

// 1. Класс Workflow - логика нашего "хихикающего" процесса
export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    const payload = event.payload;

    // Шаг 1: Получаем список файлов (бот начинает изучать код)
    const filesData = await step.do('анализ файлов', async () => {
      console.log(`Бот анализирует файлы для: ${payload.email}`);
      return {
        files: [
          'logic_v1.py',
          'bot.txt',
          'secret_sauce.js'
        ],
      };
    });

    // Шаг 2: Внешний запрос (бот сверяется с базой знаний Cloudflare)
    const apiResponse = await step.do('проверка IP', async () => {
      const resp = await fetch('https://api.cloudflare.com/client/v4/ips');
      return await resp.json<any>();
    });

    // Шаг 3: Пауза (бот хихикает над кодом 1 минуту)
    await step.sleep('бот ушел на перерыв', '1 minute');

    // Шаг 4: Попытка записи с ретраями (если упадет - попробует снова)
    await step.do(
      'финальный вердикт',
      {
        retries: {
          limit: 5,
          delay: '5 second',
          backoff: 'exponential',
        },
        timeout: '15 minutes',
      },
      async () => {
        if (Math.random() > 0.5) {
          throw new Error('Бот слишком сильно смеялся и упал!');
        }
        return { success: true, message: "Код одобрен хихиканьем!" };
      },
    );
  }
}

// 2. Входная точка для запуска Workflow через HTTP
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname === "/start") {
      const instance = await env.MY_WORKFLOW.create({
        params: {
          email: "ivan@example.com",
          metadata: { project: "solid-giggle" }
        }
      });
      return Response.json({ id: instance.id, status: "Бот запущен!" });
    }

    return new Response("Используйте /start для активации бота");
  }
};
