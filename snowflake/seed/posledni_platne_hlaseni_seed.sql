-- Seed data: SUKL drug unavailability reports for LYRICA.
-- 3 dosage variants reported as interrupted due to manufacturing issues.

INSERT INTO maisignal.l0.posledni_platne_hlaseni (
    kod_sukl, nazev, doplnek, reg, atc, typ_oznameni,
    platnost_od, datum_hlaseni, nahrazujici_lp, nahrazujici_lp_poznamka,
    duvod_preruseni_ukonceni, termin_obnoveni
)
VALUES
(0027561, 'LYRICA', '75 mg tvrdé tobolky', 'EU/1/04/279/001', 'N02BF02', 'Přerušení', '2026-03-01', '2026-03-05', 'PREGLENIX, PREGABALIN ZENTIVA, PREGABALIN MYLAN', 'Lékárny a lékaři jsou doporučeni přejít na dostupné generické alternativy. SÚKL potvrzuje bioekvivalenci všech registrovaných generik v ATC N02BF02. Zásoby LYRICA ve velkoobchodech jsou vyčerpány k 05.03.2026.', 'Výrobní problém – nedostatek účinné látky u výrobce', '2026-06-30'),
(0027562, 'LYRICA', '150 mg tvrdé tobolky', 'EU/1/04/279/004', 'N02BF02', 'Přerušení', '2026-03-01', '2026-03-05', 'PREGLENIX, PREGABALIN ZENTIVA, PREGABALIN MYLAN', 'Lékárny a lékaři jsou doporučeni přejít na dostupné generické alternativy. SÚKL potvrzuje bioekvivalenci všech registrovaných generik v ATC N02BF02. Zásoby LYRICA ve velkoobchodech jsou vyčerpány k 05.03.2026.', 'Výrobní problém – nedostatek účinné látky u výrobce', '2026-06-30'),
(0027563, 'LYRICA', '300 mg tvrdé tobolky', 'EU/1/04/279/009', 'N02BF02', 'Přerušení', '2026-03-01', '2026-03-05', 'PREGLENIX, PREGABALIN ZENTIVA, PREGABALIN MYLAN', 'Lékárny a lékaři jsou doporučeni přejít na dostupné generické alternativy. SÚKL potvrzuje bioekvivalenci všech registrovaných generik v ATC N02BF02. Zásoby LYRICA ve velkoobchodech jsou vyčerpány k 05.03.2026.', 'Výrobní problém – nedostatek účinné látky u výrobce', '2026-06-30');
