P={
"medical-malpractice":'<path d="M12 6v12a10 10 0 0 0 20 0V6"/><path d="M9 6h6M29 6h6"/><path d="M22 28v6a8 8 0 0 0 16 0v-5"/><circle cx="38" cy="25" r="4"/>',
"birth-injury":'<path d="M8 22h32a16 16 0 0 1-32 0z"/><path d="M24 22V8a14 14 0 0 1 14 14"/><path d="M14 38l-3 5M34 38l3 5"/>',
"pregnancy":'<path d="M6 40a24 24 0 0 1 36 0"/><path d="M13 42a16 16 0 0 1 22 0"/><circle cx="24" cy="16" r="6"/><path d="M18 26c3 2 9 2 12 0"/>',
"surgery":'<path d="M6 42L30 14l8 5-16 18z"/><path d="M30 14l5-8 8 5-5 8"/><path d="M12 35l5 4"/>',
"plastic-surgery":'<path d="M31 6l11 11M36 12L16 32l-6-6L30 6"/><path d="M16 32l-4 4-6-6 4-4"/><path d="M6 42l5-5"/><path d="M20 16l4 4M15 21l4 4"/>',
"bariatric-surgery":'<path d="M18 6v8c0 4-8 6-8 16a12 12 0 0 0 24 2c0-5 6-5 6-11s-6-9-12-7c-3 1-4-2-4-6V6"/><path d="M14 27h16" stroke-dasharray="2 3"/>',
"dental":'<path d="M24 12c-4-5-16-6-16 7 0 6 3 8 4 15 1 6 5 9 7 3 1-4 2-8 5-8s4 4 5 8c2 6 6 3 7-3 1-7 4-9 4-15 0-13-12-12-16-7z"/>',
"eye":'<path d="M4 24s8-13 20-13 20 13 20 13-8 13-20 13S4 24 4 24z"/><circle cx="24" cy="24" r="7"/><circle cx="24" cy="24" r="2"/>',
"cancer-diagnosis":'<path d="M16 34h20M20 34c10 0 16-6 16-14 0-5-3-9-7-11"/><path d="M19 6l8 3-6 15-8-3z"/><path d="M10 42h28M24 34v8"/>',
"road-accidents":'<path d="M18 6L6 42M30 6l12 36"/><path d="M24 8v6M24 20v7M24 33v9"/>',
"work-accidents":'<path d="M6 32h36v5H6z"/><path d="M10 32v-5a14 14 0 0 1 28 0v5"/><path d="M20 14v11M28 14v11"/>',
"national-insurance":'<path d="M24 5l16 6v12c0 10-7 17-16 20-9-3-16-10-16-20V11z"/><path d="M17 24l5 5 9-10"/>',
"disability-insurance":'<rect x="6" y="15" width="36" height="25" rx="1"/><path d="M17 15v-5h14v5"/><path d="M6 26h36M24 23v6"/>',
"insurance-claims":'<path d="M11 5h20l8 8v30H11z"/><path d="M31 5v8h8"/><path d="M17 21h15M17 28h15M17 35h8"/>',
"statute-of-limitations":'<path d="M12 5h24M12 43h24"/><path d="M15 5v8c0 6 9 8 9 11s-9 5-9 11v8M33 5v8c0 6-9 8-9 11s9 5 9 11v8"/><path d="M19 38c2-3 8-3 10 0"/>',
"medical-opinion":'<path d="M10 5h22v38H10z"/><path d="M16 14h10M16 21h10M16 28h6"/><path d="M38 14l4 4-14 16-5 1 1-5z"/>',
"medical-records":'<path d="M5 12h14l4 5h20v25H5z"/><path d="M24 24v11M18.500 29.500h11"/>',
"contact":'<path d="M6 8h36v26H22l-9 8v-8H6z"/>',
}
def icon(slug,cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{P.get(slug,P["contact"])}</svg>'
