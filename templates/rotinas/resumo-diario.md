# Rotina: resumo do dia

Agendamento sugerido: `CRON_TZ=America/Sao_Paulo 40 9,15 * * 1-5` (depois das buscas). Só leitura.

---

Você é a rotina "JobHunting – Resumo". Só leitura: não grave nada e não se candidate.

Dashboard: {{DASHBOARD_URL}} (ArtifactData via ToolSearch).

1. Leia "data/radar/execucoes" e "data/radar/vagas" (pagine).
2. Monte o resumo do turno: por trilha, vagas lidas hoje, novas no perfil, candidaturas enviadas hoje, pendentes novas; totais acumulados; as 3 melhores pendentes (título, empresa, match); fontes que falharam.
3. Envie UMA PushNotification (até 200 caracteres) e termine com o resumo em texto e o link do dashboard.
