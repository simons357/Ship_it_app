"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import {
  CUSTOM_ID,
  shipActionOptions,
  shipToOptions,
  type ShipChoice,
} from "@/lib/ship/options";

type Step = 1 | 2 | 3;

type ShipResult = {
  to: string;
  action: string;
  note: string;
  fileName?: string;
  detail?: string;
};

function ChoiceList({
  options,
  selectedId,
  customValue,
  customPlaceholder,
  onSelectPreset,
  onSelectCustom,
  onCustomChange,
}: {
  options: ShipChoice[];
  selectedId: string | null;
  customValue: string;
  customPlaceholder: string;
  onSelectPreset: (option: ShipChoice) => void;
  onSelectCustom: () => void;
  onCustomChange: (value: string) => void;
}) {
  const customRef = useRef<HTMLInputElement>(null);
  const isCustom = selectedId === CUSTOM_ID;

  useEffect(() => {
    if (isCustom) {
      customRef.current?.focus();
    }
  }, [isCustom]);

  return (
    <div className="space-y-3">
      <ul className="divide-y divide-line border-y border-line">
        {options.map((option) => {
          const active = selectedId === option.id;
          return (
            <li key={option.id}>
              <button
                type="button"
                onClick={() => onSelectPreset(option)}
                className={`flex w-full flex-col gap-0.5 py-4 text-left transition-colors hover:bg-mist/60 ${
                  active ? "bg-mist/80" : ""
                }`}
              >
                <span className="font-medium text-ink">{option.label}</span>
                <span className="text-sm text-ink-soft">{option.hint}</span>
              </button>
            </li>
          );
        })}
        <li>
          <button
            type="button"
            onClick={onSelectCustom}
            className={`flex w-full flex-col gap-0.5 py-4 text-left transition-colors hover:bg-mist/60 ${
              isCustom ? "bg-mist/80" : ""
            }`}
          >
            <span className="font-medium text-ink">Custom</span>
            <span className="text-sm text-ink-soft">
              Type exactly what you need
            </span>
          </button>
        </li>
      </ul>

      <label className="block">
        <span className="sr-only">Your answer</span>
        <input
          ref={customRef}
          value={customValue}
          onChange={(event) => {
            onSelectCustom();
            onCustomChange(event.target.value);
          }}
          onFocus={onSelectCustom}
          placeholder={customPlaceholder}
          className="w-full rounded-md border border-line bg-foam px-4 py-3.5 text-base text-ink outline-none transition-shadow focus:border-sea focus:ring-2 focus:ring-sea/20"
        />
      </label>
    </div>
  );
}

export function ShipFlow() {
  const [step, setStep] = useState<Step>(1);
  const [toId, setToId] = useState<string | null>(null);
  const [toValue, setToValue] = useState("");
  const [actionId, setActionId] = useState<string | null>(null);
  const [actionValue, setActionValue] = useState("");
  const [detail, setDetail] = useState("");
  const [fileName, setFileName] = useState("");
  const [note, setNote] = useState("");
  const [status, setStatus] = useState<"idle" | "shipping" | "done">("idle");
  const [result, setResult] = useState<ShipResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  function goNext() {
    setError(null);
    if (step === 1) {
      if (!toValue.trim()) {
        setError("Tell me where this should go — pick one or type Custom.");
        return;
      }
      setStep(2);
      return;
    }
    if (step === 2) {
      if (!actionValue.trim()) {
        setError("Say what you want to happen — pick one or type Custom.");
        return;
      }
      setStep(3);
    }
  }

  function goBack() {
    setError(null);
    if (step === 2) setStep(1);
    if (step === 3) setStep(2);
  }

  async function handleShip(event: FormEvent) {
    event.preventDefault();
    setError(null);

    if (!note.trim()) {
      setError("Add a short note — even one line is enough.");
      return;
    }

    setStatus("shipping");
    await new Promise((resolve) => setTimeout(resolve, 650));

    const shipped: ShipResult = {
      to: toValue.trim(),
      action: actionValue.trim(),
      note: note.trim(),
      fileName: fileName || undefined,
      detail: detail.trim() || undefined,
    };

    setResult(shipped);
    setStatus("done");
  }

  function reset() {
    setStep(1);
    setToId(null);
    setToValue("");
    setActionId(null);
    setActionValue("");
    setDetail("");
    setFileName("");
    setNote("");
    setStatus("idle");
    setResult(null);
    setError(null);
  }

  if (status === "done" && result) {
    return (
      <div className="ship-confirm mx-auto w-full max-w-xl">
        <p className="font-mono text-xs uppercase tracking-[0.22em] text-sea-deep">
          Taken care of
        </p>
        <h1 className="mt-4 font-[family-name:var(--font-display)] text-4xl font-semibold tracking-tight text-ink sm:text-5xl">
          Shipped.
        </h1>
        <p className="mt-4 text-lg text-ink-soft">Boom — it’s off your plate.</p>

        <dl className="mt-10 space-y-5 border-y border-line py-6 text-sm">
          <div>
            <dt className="font-mono text-xs uppercase tracking-[0.16em] text-ink-soft">
              To
            </dt>
            <dd className="mt-1 text-base text-ink">{result.to}</dd>
          </div>
          <div>
            <dt className="font-mono text-xs uppercase tracking-[0.16em] text-ink-soft">
              What happens
            </dt>
            <dd className="mt-1 text-base text-ink">{result.action}</dd>
          </div>
          {result.fileName || result.detail ? (
            <div>
              <dt className="font-mono text-xs uppercase tracking-[0.16em] text-ink-soft">
                Payload
              </dt>
              <dd className="mt-1 text-base text-ink">
                {[result.fileName, result.detail].filter(Boolean).join(" · ")}
              </dd>
            </div>
          ) : null}
          <div>
            <dt className="font-mono text-xs uppercase tracking-[0.16em] text-ink-soft">
              Note
            </dt>
            <dd className="mt-1 text-base text-ink">{result.note}</dd>
          </div>
        </dl>

        <p className="mt-6 text-sm text-ink-soft">
          Demo mode confirms locally. Live send destinations come next.
        </p>

        <button
          type="button"
          onClick={reset}
          className="mt-8 rounded-md bg-sea px-6 py-3 text-base font-semibold text-foam transition-transform transition-colors hover:bg-sea-deep hover:scale-[1.02] active:scale-[0.99]"
        >
          Ship another
        </button>
      </div>
    );
  }

  return (
    <div className="mx-auto w-full max-w-xl">
      <div className="mb-8 flex items-end justify-between gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.22em] text-sea-deep">
            Step {step} of 3
          </p>
          <div
            className="mt-3 h-1 w-40 overflow-hidden rounded-full bg-mist"
            aria-hidden="true"
          >
            <div
              className="h-full bg-sea transition-all duration-500 ease-out"
              style={{ width: `${(step / 3) * 100}%` }}
            />
          </div>
        </div>
        {step > 1 ? (
          <button
            type="button"
            onClick={goBack}
            className="text-sm text-ink-soft transition-colors hover:text-ink"
          >
            Back
          </button>
        ) : null}
      </div>

      {step === 1 ? (
        <section className="hero-rise">
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            Ship it to?
          </h1>
          <p className="mt-3 text-base text-ink-soft">
            One answer. Pick a standard path or type Custom.
          </p>
          <div className="mt-8">
            <ChoiceList
              options={shipToOptions}
              selectedId={toId}
              customValue={toValue}
              customPlaceholder="e.g. Maya’s inbox, client Dropbox, Friday folder…"
              onSelectPreset={(option) => {
                setToId(option.id);
                setToValue(option.label);
                setError(null);
              }}
              onSelectCustom={() => setToId(CUSTOM_ID)}
              onCustomChange={(value) => {
                setToValue(value);
                setError(null);
              }}
            />
          </div>
          {error ? (
            <p className="mt-4 text-sm text-signal" role="alert">
              {error}
            </p>
          ) : null}
          <button
            type="button"
            onClick={goNext}
            className="mt-8 w-full rounded-md bg-sea px-6 py-3 text-base font-semibold text-foam transition-transform transition-colors hover:bg-sea-deep hover:scale-[1.01] active:scale-[0.99]"
          >
            Continue
          </button>
        </section>
      ) : null}

      {step === 2 ? (
        <section className="hero-rise">
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            What do you want to happen?
          </h1>
          <p className="mt-3 text-base text-ink-soft">
            Put the outcome in the box. Attach something if you need to.
          </p>
          <div className="mt-8">
            <ChoiceList
              options={shipActionOptions}
              selectedId={actionId}
              customValue={actionValue}
              customPlaceholder="e.g. Send the final PDF, drop the link, archive this…"
              onSelectPreset={(option) => {
                setActionId(option.id);
                setActionValue(option.label);
                setError(null);
              }}
              onSelectCustom={() => setActionId(CUSTOM_ID)}
              onCustomChange={(value) => {
                setActionValue(value);
                setError(null);
              }}
            />
          </div>

          <div className="mt-8 space-y-4 border-t border-line pt-8">
            <label className="block">
              <span className="text-sm font-medium text-ink">
                File (optional)
              </span>
              <input
                type="file"
                onChange={(event) =>
                  setFileName(event.target.files?.[0]?.name ?? "")
                }
                className="mt-2 block w-full text-sm text-ink-soft file:mr-4 file:rounded-md file:border-0 file:bg-sea file:px-4 file:py-2 file:text-sm file:font-medium file:text-foam hover:file:bg-sea-deep"
              />
              {fileName ? (
                <span className="mt-2 block text-sm text-ink-soft">
                  Ready: {fileName}
                </span>
              ) : null}
            </label>
            <label className="block">
              <span className="text-sm font-medium text-ink">
                Link or extra detail (optional)
              </span>
              <input
                value={detail}
                onChange={(event) => setDetail(event.target.value)}
                placeholder="https://… or a short detail"
                className="mt-2 w-full rounded-md border border-line bg-foam px-4 py-3 text-ink outline-none transition-shadow focus:border-sea focus:ring-2 focus:ring-sea/20"
              />
            </label>
          </div>

          {error ? (
            <p className="mt-4 text-sm text-signal" role="alert">
              {error}
            </p>
          ) : null}
          <button
            type="button"
            onClick={goNext}
            className="mt-8 w-full rounded-md bg-sea px-6 py-3 text-base font-semibold text-foam transition-transform transition-colors hover:bg-sea-deep hover:scale-[1.01] active:scale-[0.99]"
          >
            Continue
          </button>
        </section>
      ) : null}

      {step === 3 ? (
        <section className="hero-rise">
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            Semi-personal note
          </h1>
          <p className="mt-3 text-base text-ink-soft">
            A human line — warm enough, short enough. Then ship.
          </p>

          <form onSubmit={handleShip} className="mt-8 space-y-6">
            <label className="block">
              <span className="sr-only">Note</span>
              <textarea
                value={note}
                onChange={(event) => {
                  setNote(event.target.value);
                  setError(null);
                }}
                rows={5}
                placeholder="Hey — finished piece is attached. Take a look when you can."
                className="w-full resize-y rounded-md border border-line bg-foam px-4 py-3.5 text-base leading-relaxed text-ink outline-none transition-shadow focus:border-sea focus:ring-2 focus:ring-sea/20"
              />
            </label>

            <div className="border border-line bg-mist/50 px-4 py-4 text-sm text-ink-soft">
              <p>
                <span className="font-medium text-ink">To:</span> {toValue}
              </p>
              <p className="mt-1">
                <span className="font-medium text-ink">What:</span>{" "}
                {actionValue}
              </p>
            </div>

            {error ? (
              <p className="text-sm text-signal" role="alert">
                {error}
              </p>
            ) : (
              <p className="text-sm text-ink-soft">
                One tap from done. No hunting through menus.
              </p>
            )}

            <button
              type="submit"
              disabled={status === "shipping"}
              className="w-full rounded-md bg-sea px-6 py-3 text-base font-semibold text-foam transition-transform transition-colors hover:bg-sea-deep hover:scale-[1.01] active:scale-[0.99] disabled:cursor-wait disabled:opacity-70"
            >
              {status === "shipping" ? "Shipping…" : "Ship it"}
            </button>
          </form>
        </section>
      ) : null}
    </div>
  );
}
