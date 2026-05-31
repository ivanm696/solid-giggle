import { WorkflowEntrypoint, WorkflowEvent, WorkflowStep } from 'cloudflare:workers';

/**
 * Окружение (Bindings)
 */
interface Env {
  MY_WORKFLOW: Workflow;
}

/**
 * Параметры, передаваемые в Workflow
 */
interface Params {
  email: string;
  metadata: Record<string, string>;
}

/**
 * Основной класс Workflow
 */
export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    const { email, metadata } = event.payload;

    // Шаг 1: Имитация получения списка файлов
    const filesData = await step.do("fetch files list", async () => {
      return { files: ["file1.pdf", "file2.jpg"], count: 2 };
    });

    // Шаг 2: Внешний API запрос (Cloudflare IPs)
    const apiData = await step.do("get cloudflare ips", async () => {
      const response = await fetch("https://api.cloudflare.com/client/v4/ips");
      if (!response.ok) throw new Error("API request failed");
      return await response.json();
    });

    // Шаг 3: Ожидание 1 минуту
    await step.sleep("wait for processing", "1 minute");

    // Шаг 4: Надежная запись с политикой ретраев (до 5 попыток)
    await step.do(
      "reliable write operation",
      {
        retries: {
          limit: 5,
          delay: "2 seconds",
          backoff: "exponential",
        },
      },
      async () => {
        // Имитация случайного сбоя для проверки ретраев
        if (Math.random() > 0.5) {
          throw new Error("Temporary storage failure");
        }
        return { status: "success" };
      }
    );
  }
}

/**
 * HTTP обработчик для ручного запуска Workflow
 */
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/start") {
      const instance = await env.MY_WORKFLOW.create({
        params: {
          email: "user@example.com",
          metadata: { project: "giggle_engine" }
        }
      });
      return new Response(JSON.stringify({ workflowId: instance.id }), {
        headers: { "Content-Type": "application/json" }
      });
    }

    return new Response("Send GET to /start to trigger Workflow");
  },
};
