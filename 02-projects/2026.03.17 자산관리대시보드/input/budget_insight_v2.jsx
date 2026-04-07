import { useState, useMemo } from "react";

// ════════════════════════════════════════
// DATA
// ════════════════════════════════════════
const PLANS = {
  2025: {
    수입:{상여금:6440000,월급여:7420000,기타수입:400000},
    저축성:{주담대원금:1500000,적금:1000000,주식투자:5800000,연금저축:800000,기타:200000,기타2:150000},
    순지출:{"생활비/대출이자":2500000,경조사비:450000,식비:300000,교통비:200000,"의복/미용":200000,"문화/여가":100000,"카페/간식":200000,"주거/통신":160000,"의료/건강":170000,기타:400000},
  },
  2026: {
    수입:{상여금:4200000,월급여:13900000,기타수입:450000},
    저축성:{주담대원금:1500000,적금:1000000,주식투자:9100000,연금저축:1000000,연금보험:200000,개인투자:880000},
    순지출:{"생활비/대출이자":2500000,경조사비:400000,식비:200000,교통비:200000,"의복/미용":250000,"문화/여가":100000,"카페/간식":200000,"주거/통신":100000,"의료/건강":200000,기타:400000},
  }
};

const RAW = {
  2025: {
    year:2025, mc:12,
    수입:{
      상여금:[7156600,7205600,0,7376400,7239900,7239100,11775100,0,3880200,3801000,3836200,0],
      월급여:[7327000,7502800,7910200,7323500,7749600,8021300,12108232,13534610,14432300,14058400,13911710,20876766],
      기타수입:[3201859,232572,515342,616921,2233568,1405824,41779607,800316,1143691,748903,743407,743407],
    },
    저축성:{
      주담대원금:[1500000,1500000,1500000,1500000,1500000,1500000,1500000,1500000,1500000,1500000,1500000,1500000],
      적금:[2400000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000],
      주식투자:[10800000,5800000,5800000,5900000,5900000,5900000,7900000,8500000,8500000,4400000,4400000,8500000],
      연금저축:[400000,800000,400000,400000,400000,400000,400000,400000,400000,400000,400000,400000],
      기타:[200000,200000,200000,200000,200000,200000,200000,200000,200000,200000,200000,200000],
      기타2:[150000,150000,150000,150000,150000,150000,150000,150000,150000,150000,150000,150000],
    },
    순지출:{
      "생활비/대출이자":[3700000,2500000,2500000,2500000,3300000,3700000,2500000,2500000,2500000,2500000,2500000,3000000],
      "이자(일반대)":[0,0,27,0,0,0,0,0,0,172,0,0],
      경조사비:[205000,110000,110000,830000,249874,258572,575000,610000,179900,57900,520000,520000],
      식비:[205200,294730,225970,402400,436615,199272,80940,144400,195500,140730,153000,153000],
      교통비:[393808,303360,244890,214410,201440,250772,370265,297503,110779,183714,259795,259795],
      "의복/미용":[0,123500,10900,492300,345983,704786,370864,399857,0,316012,246176,246176],
      "문화/여가":[13300,76180,13000,20400,13300,117300,42220,493600,37800,17875,234824,234824],
      "카페/간식":[186430,218125,303580,190280,285762,139050,138080,93150,102880,124400,252910,252910],
      "주거/통신":[62000,150790,107010,106200,62000,115780,94030,44000,64350,64350,64350,64350],
      "의료/건강":[375867,280088,175646,141546,174776,152546,141546,141546,643846,1318803,4642841,4642841],
      기타:[0,0,0,123500,1856343,1411733,12889830,1620462,0,40000,635000,635000],
    },
  },
  2026: {
    year:2026, mc:2,
    수입:{
      상여금:[24330110,3905300],
      월급여:[6368790,8377967],
      기타수입:[671821,17620048],
    },
    저축성:{
      주담대원금:[1500000,1500000],
      적금:[1000000,500000],
      주식투자:[9100000,9100000],
      연금저축:[1000000,1000000],
      연금보험:[200000,200000],
      개인투자:[860000,800000],
    },
    순지출:{
      "생활비/대출이자":[2500000,3000000],
      "이자(일반대)":[2536,241],
      경조사비:[42400,972880],
      식비:[325277,149400],
      교통비:[230637,81270],
      "의복/미용":[154043,4429973],
      "문화/여가":[13300,13308],
      "카페/간식":[110100,113500],
      "주거/통신":[64520,64350],
      "의료/건강":[150844,368998],
      기타:[124040,2377400],
    },
  }
};

// ════════════════════════════════════════
// HELPERS
// ════════════════════════════════════════
const S = a => a.reduce((x,y)=>x+(y||0),0);
const fmt = n => {if(n==null)return"—";const a=Math.abs(n);if(a>=1e8)return(n/1e8).toFixed(1)+"억";if(a>=1e4)return Math.round(n/1e4).toLocaleString()+"만";return Math.round(n).toLocaleString()+"원"};
const fmtK = n => n!=null?Math.round(n).toLocaleString():"—";
const pct = (a,b) => b?(a/b*100).toFixed(1)+"%":"—";
const pctN = (a,b) => b?(a/b*100):0;
const ML = ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"];
const CL = {"생활비/대출이자":"#ef4444",경조사비:"#f97316",식비:"#eab308",교통비:"#84cc16","의복/미용":"#06b6d4","문화/여가":"#8b5cf6","카페/간식":"#ec4899","주거/통신":"#6366f1","의료/건강":"#14b8a6",기타:"#94a3b8","이자(일반대)":"#64748b"};

function proc(raw) {
  const n=raw.mc;
  const 수입계=Array(n).fill(0), 저축계=Array(n).fill(0), 지출계=Array(n).fill(0);
  Object.values(raw.수입).forEach(a=>a.forEach((v,i)=>수입계[i]+=v));
  Object.values(raw.저축성).forEach(a=>a.forEach((v,i)=>저축계[i]+=v));
  Object.values(raw.순지출).forEach(a=>a.forEach((v,i)=>지출계[i]+=v));
  const 여유=수입계.map((v,i)=>v-저축계[i]-지출계[i]);
  return {...raw, 수입계, 저축계, 지출계, 여유};
}

// ════════════════════════════════════════
// SUB COMPONENTS
// ════════════════════════════════════════
const C = {bg:"#f5f6f8",card:"#fff",border:"#e8eaed",t1:"#1a1a2e",t2:"#555",t3:"#888",t4:"#bbb",
  green:"#10b981",blue:"#6366f1",amber:"#f59e0b",red:"#ef4444",cyan:"#06b6d4",purple:"#8b5cf6"};

function Tabs({items,active,onChange,size="md"}) {
  const s = size==="sm" ? {p:"4px 10px",fs:10,br:12} : {p:"6px 16px",fs:12,br:16};
  return (
    <div style={{display:"flex",gap:4,flexWrap:"wrap"}}>
      {items.map(it => (
        <button key={it.key} onClick={()=>onChange(it.key)} style={{padding:s.p,borderRadius:s.br,border:"1px solid",cursor:"pointer",fontWeight:600,fontSize:s.fs,transition:"all .15s",
          background:active===it.key?C.t1:C.card,color:active===it.key?"#fff":C.t2,borderColor:active===it.key?C.t1:C.border}}>{it.label}</button>
      ))}
    </div>
  );
}

function Card({children,style}) {
  return <div style={{background:C.card,borderRadius:14,padding:18,border:`1px solid ${C.border}`,...style}}>{children}</div>;
}

function Kpi({icon,label,value,sub,color}) {
  return (
    <div style={{background:C.card,borderRadius:12,padding:"14px 16px",border:`1px solid ${C.border}`,position:"relative",overflow:"hidden"}}>
      <div style={{position:"absolute",top:0,left:0,right:0,height:3,background:color}}/>
      <div style={{fontSize:9,color:C.t3,fontWeight:600,letterSpacing:.5,textTransform:"uppercase"}}>{icon} {label}</div>
      <div style={{fontSize:20,fontWeight:800,color,fontFamily:"monospace",margin:"4px 0 2px"}}>{value}</div>
      {sub && <div style={{fontSize:10,color:C.t4}}>{sub}</div>}
    </div>
  );
}

function Bar({value,max,color,height=14}) {
  const w = max ? Math.min(Math.abs(value)/max*100,100) : 0;
  return <div style={{background:"#f0f1f5",borderRadius:6,height,overflow:"hidden"}}><div style={{width:w+"%",height:"100%",background:color,borderRadius:6,transition:"width .4s"}}/></div>;
}

function PlanVsActualRow({label,plan,actual,color}) {
  const diff = actual - plan;
  const diffPct = plan ? (diff/plan*100) : 0;
  const over = actual > plan;
  return (
    <div style={{display:"flex",alignItems:"center",gap:8,padding:"6px 0",borderBottom:`1px solid ${C.border}`,fontSize:11}}>
      <div style={{width:10,height:10,borderRadius:"50%",background:color||C.blue,flexShrink:0}}/>
      <div style={{flex:"0 0 110px",fontWeight:600,color:C.t2}}>{label}</div>
      <div style={{flex:"0 0 80px",textAlign:"right",color:C.t3,fontFamily:"monospace",fontSize:10}}>{fmtK(plan)}</div>
      <div style={{flex:1}}><Bar value={actual} max={Math.max(plan,actual)*1.1} color={color||C.blue}/></div>
      <div style={{flex:"0 0 80px",textAlign:"right",fontWeight:700,fontFamily:"monospace",fontSize:10}}>{fmtK(actual)}</div>
      <div style={{flex:"0 0 65px",textAlign:"right",fontSize:10,fontWeight:600,
        color:label.includes("지출")||Object.keys(CL).includes(label) ? (over?C.red:C.green) : (over?C.green:C.amber)}}>
        {diff>=0?"+":""}{diffPct.toFixed(0)}%
      </div>
    </div>
  );
}

// ════════════════════════════════════════
// MAIN TABS
// ════════════════════════════════════════
function TabOverview({data,yr,mo}) {
  const 수입=data.수입계[mo], 저축=data.저축계[mo], 지출=data.지출계[mo], 여유=data.여유[mo];
  
  // Insights
  const ins = [];
  const 지출률=pctN(지출,수입), 저축률=pctN(저축,수입);
  if(지출률>40)ins.push({t:"alert",s:`⚠️ 지출 비중 ${지출률.toFixed(0)}% — 수입의 40% 초과`,b:`비경상 지출 항목을 확인해보세요.`});
  else if(지출률<25)ins.push({t:"good",s:`✅ 지출 통제 우수 (${지출률.toFixed(0)}%)`,b:`25% 미만으로 잘 관리되고 있습니다.`});
  if(저축률>50)ins.push({t:"good",s:`💰 저축률 ${저축률.toFixed(0)}% 달성`,b:`50% 이상의 높은 저축률입니다.`});
  if(여유<0)ins.push({t:"alert",s:"🔴 여유자금 적자 발생",b:`수입보다 저축+지출이 ${fmt(Math.abs(여유))} 초과했습니다.`});
  if(mo>0){
    const pd=data.지출계[mo-1]; const ch=pd?(지출-pd)/pd*100:0;
    if(ch>50)ins.push({t:"alert",s:`📈 전월 대비 지출 ${ch.toFixed(0)}% 급증`,b:`${mo}월→${mo+1}월 지출 ${fmt(지출-pd)} 증가`});
  }
  const topCat = Object.entries(data.순지출).map(([k,a])=>({k,v:a[mo]||0})).sort((a,b)=>b.v-a.v)[0];
  if(topCat && 지출 && topCat.v/지출>0.4)ins.push({t:"warn",s:`📊 "${topCat.k}" 집중 (${(topCat.v/지출*100).toFixed(0)}%)`,b:`단일 항목이 지출의 40% 이상입니다.`});

  // Donut data
  const items = Object.entries(data.순지출).map(([k,a])=>({k,v:a[mo]||0,c:CL[k]||"#94a3b8"})).filter(x=>x.v>0).sort((a,b)=>b.v-a.v);
  const total = S(items.map(x=>x.v));
  let cum=0;
  const slices = items.map(it=>{const a=(it.v/total)*360;const s=cum;cum+=a;return{...it,s,a}});
  const arc=(cx,cy,r,s,e)=>{const tr=d=>d*Math.PI/180;const sr=tr(s-90),er=tr(e-90);return`M${cx},${cy} L${cx+r*Math.cos(sr)},${cy+r*Math.sin(sr)} A${r},${r} 0 ${e-s>180?1:0} 1 ${cx+r*Math.cos(er)},${cy+r*Math.sin(er)} Z`};

  return (
    <div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10,marginBottom:14}}>
        <Kpi icon="💵" label="수입" value={fmt(수입)} sub={`전체 기준`} color={C.green}/>
        <Kpi icon="🏦" label="저축" value={fmt(저축)} sub={`저축률 ${pct(저축,수입)}`} color={C.blue}/>
        <Kpi icon="💳" label="지출" value={fmt(지출)} sub={`지출률 ${pct(지출,수입)}`} color={C.amber}/>
        <Kpi icon="✨" label="여유" value={fmt(여유)} sub={`여유율 ${pct(Math.max(0,여유),수입)}`} color={여유>=0?C.cyan:C.red}/>
      </div>

      {ins.length>0 && (
        <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8,marginBottom:14}}>
          {ins.map((x,i)=>(
            <div key={i} style={{background:C.card,border:`1px solid ${C.border}`,borderRadius:10,padding:12,borderLeft:`3px solid ${x.t==="alert"?C.red:x.t==="good"?C.green:C.amber}`}}>
              <div style={{fontSize:11,fontWeight:700,marginBottom:2}}>{x.s}</div>
              <div style={{fontSize:10,color:C.t3,lineHeight:1.5}}>{x.b}</div>
            </div>
          ))}
        </div>
      )}

      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:14}}>
        <Card>
          <div style={{fontSize:13,fontWeight:700,marginBottom:10}}>{yr}년 {mo+1}월 지출 구성</div>
          <div style={{display:"flex",gap:14,alignItems:"center"}}>
            <svg width={130} height={130} viewBox="0 0 130 130">
              {slices.map((s,i)=><path key={i} d={arc(65,65,60,s.s,s.s+s.a-.5)} fill={s.c} opacity={.85}><title>{s.k}: {fmt(s.v)}</title></path>)}
              <circle cx={65} cy={65} r={36} fill="#fff"/>
              <text x={65} y={62} textAnchor="middle" fontSize={12} fontWeight={800} fill={C.t1}>{fmt(total)}</text>
              <text x={65} y={75} textAnchor="middle" fontSize={8} fill={C.t3}>총지출</text>
            </svg>
            <div style={{flex:1,fontSize:10}}>
              {items.slice(0,7).map((it,i)=>(
                <div key={i} style={{display:"flex",justifyContent:"space-between",padding:"3px 0",borderBottom:`1px solid #f5f5f5`}}>
                  <span style={{display:"flex",alignItems:"center",gap:5}}><span style={{width:7,height:7,borderRadius:"50%",background:it.c,display:"inline-block"}}/>{it.k}</span>
                  <span style={{fontWeight:600,fontFamily:"monospace"}}>{fmt(it.v)}<span style={{color:C.t4,fontWeight:400}}> ({pct(it.v,total)})</span></span>
                </div>
              ))}
            </div>
          </div>
        </Card>

        <div style={{display:"flex",flexDirection:"column",gap:10}}>
          <div style={{background:"#f8f9fb",borderRadius:10,padding:14,border:`1px solid ${C.border}`}}>
            <div style={{fontSize:12,fontWeight:700,color:C.t2,marginBottom:8}}>{yr}년 {mo+1}월 수입 배분</div>
            <div style={{display:"flex",borderRadius:6,overflow:"hidden",height:20,background:"#eee"}}>
              {[{l:"저축",v:저축,c:C.blue},{l:"지출",v:지출,c:C.amber},{l:"여유",v:Math.max(0,여유),c:C.cyan}].map((x,i)=>(
                <div key={i} style={{width:pct(x.v,수입),background:x.c,minWidth:1,transition:"width .3s"}} title={`${x.l}: ${fmt(x.v)}`}/>
              ))}
            </div>
            <div style={{display:"flex",justifyContent:"space-between",fontSize:9,color:C.t4,marginTop:4}}>
              <span>저축 {pct(저축,수입)}</span><span>지출 {pct(지출,수입)}</span><span>여유 {pct(Math.max(0,여유),수입)}</span>
            </div>
          </div>

          <Card style={{flex:1}}>
            <div style={{fontSize:12,fontWeight:700,marginBottom:6}}>월별 여유자금 추이</div>
            <svg viewBox="0 0 100 55" style={{width:"100%",height:90}}>
              {data.여유.map((v,i)=>{
                const mx=Math.max(...data.여유.map(Math.abs),1);
                const h=(Math.abs(v)/mx)*40; const x=(i+.5)*(100/data.mc); const bw=100/(data.mc*1.6);
                return <g key={i}><rect x={x-bw/2} y={v>=0?45-h:45} width={bw} height={h} fill={v>=0?C.cyan:C.red} rx={2} opacity={i===mo?1:.5}><title>{ML[i]}: {fmt(v)}</title></rect>
                  <text x={x} y={53} textAnchor="middle" fontSize={3.2} fill={C.t4}>{i+1}</text></g>;
              })}
              <line x1={0} y1={45} x2={100} y2={45} stroke={C.border} strokeWidth={.3}/>
            </svg>
          </Card>
        </div>
      </div>
    </div>
  );
}

function TabPlanVsActual({data,yr,mo}) {
  const plan = PLANS[yr];
  if(!plan) return <div style={{padding:40,textAlign:"center",color:C.t3}}>해당 연도 계획 데이터 없음</div>;
  
  const mc = data.mc;
  const monthlyPlan = (v) => v; // plan is monthly
  
  // Build comparison for selected month
  const 수입실 = data.수입계[mo], 수입계 = S(Object.values(plan.수입));
  const 저축실 = data.저축계[mo], 저축계 = S(Object.values(plan.저축성));
  const 지출실 = data.지출계[mo], 지출계 = S(Object.values(plan.순지출));

  // YTD comparison
  const ytdActInc = S(data.수입계), ytdPlanInc = 수입계 * mc;
  const ytdActSav = S(data.저축계), ytdPlanSav = 저축계 * mc;
  const ytdActExp = S(data.지출계), ytdPlanExp = 지출계 * mc;

  return (
    <div>
      {/* Summary KPIs */}
      <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:10,marginBottom:14}}>
        {[
          {l:"수입",pl:수입계,ac:수입실,c:C.green},
          {l:"저축성",pl:저축계,ac:저축실,c:C.blue},
          {l:"순지출",pl:지출계,ac:지출실,c:C.amber},
        ].map((x,i)=>{
          const d=x.ac-x.pl, dp=x.pl?(d/x.pl*100):0;
          const isExpense = x.l==="순지출";
          const good = isExpense ? d<0 : d>0;
          return (
            <Card key={i} style={{textAlign:"center"}}>
              <div style={{fontSize:10,color:C.t3,fontWeight:600}}>{x.l}</div>
              <div style={{display:"flex",justifyContent:"center",gap:16,margin:"8px 0"}}>
                <div><div style={{fontSize:9,color:C.t4}}>계획</div><div style={{fontSize:15,fontWeight:700,color:C.t3,fontFamily:"monospace"}}>{fmt(x.pl)}</div></div>
                <div style={{fontSize:18,color:C.t4,alignSelf:"center"}}>→</div>
                <div><div style={{fontSize:9,color:C.t4}}>실적</div><div style={{fontSize:15,fontWeight:800,color:x.c,fontFamily:"monospace"}}>{fmt(x.ac)}</div></div>
              </div>
              <div style={{fontSize:11,fontWeight:700,color:good?C.green:C.red,background:good?"rgba(16,185,129,.08)":"rgba(239,68,68,.08)",padding:"3px 10px",borderRadius:8,display:"inline-block"}}>
                {d>=0?"+":""}{dp.toFixed(0)}% ({d>=0?"+":""}{fmt(d)})
              </div>
            </Card>
          );
        })}
      </div>

      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:14}}>
        {/* Monthly detail */}
        <Card>
          <div style={{fontSize:13,fontWeight:700,marginBottom:4}}>{yr}년 {mo+1}월 항목별 계획 vs 실적</div>
          <div style={{fontSize:10,color:C.t4,marginBottom:10}}>지출 항목 — 계획 초과 시 빨간색 표시</div>
          {Object.entries(plan.순지출).map(([k,v])=>{
            const actual = data.순지출[k]?.[mo]||0;
            return <PlanVsActualRow key={k} label={k} plan={v} actual={actual} color={CL[k]}/>;
          })}
          <div style={{borderTop:`2px solid ${C.border}`,marginTop:4,paddingTop:6,display:"flex",justifyContent:"space-between",fontSize:11,fontWeight:700}}>
            <span>합계</span>
            <span style={{color:C.t3}}>계획 {fmt(지출계)}</span>
            <span style={{color:지출실>지출계?C.red:C.green}}>실적 {fmt(지출실)} ({지출실>지출계?"+":""}{((지출실-지출계)/지출계*100).toFixed(0)}%)</span>
          </div>
        </Card>

        {/* YTD Plan vs Actual chart */}
        <Card>
          <div style={{fontSize:13,fontWeight:700,marginBottom:4}}>{yr}년 누적 계획 vs 실적 ({mc}개월)</div>
          <div style={{fontSize:10,color:C.t4,marginBottom:12}}>연간 계획금액 × {mc}개월 기준</div>
          {[
            {l:"수입",pa:ytdPlanInc,ac:ytdActInc,c:C.green},
            {l:"저축",pa:ytdPlanSav,ac:ytdActSav,c:C.blue},
            {l:"지출",pa:ytdPlanExp,ac:ytdActExp,c:C.amber},
          ].map((x,i)=>{
            const mx = Math.max(x.pa,x.ac)*1.15;
            const isExp = x.l==="지출";
            const good = isExp ? x.ac<=x.pa : x.ac>=x.pa;
            return (
              <div key={i} style={{marginBottom:16}}>
                <div style={{display:"flex",justifyContent:"space-between",fontSize:11,marginBottom:4}}>
                  <span style={{fontWeight:600}}>{x.l}</span>
                  <span style={{fontSize:10,fontWeight:600,color:good?C.green:C.red}}>{good?"✅":"⚠️"} 실적 {fmt(x.ac)}</span>
                </div>
                <div style={{position:"relative",height:22,background:"#f5f5f5",borderRadius:6}}>
                  <div style={{position:"absolute",height:"100%",width:(x.pa/mx*100)+"%",background:"rgba(0,0,0,.06)",borderRadius:6,borderRight:"2px dashed "+C.t4}}/>
                  <div style={{position:"absolute",height:"100%",width:(x.ac/mx*100)+"%",background:x.c,borderRadius:6,opacity:.75,transition:"width .4s"}}/>
                </div>
                <div style={{display:"flex",justifyContent:"space-between",fontSize:9,color:C.t4,marginTop:2}}>
                  <span>계획 {fmt(x.pa)}</span>
                  <span>달성률 {pct(x.ac,x.pa)}</span>
                </div>
              </div>
            );
          })}

          {/* Monthly plan vs actual bar chart */}
          <div style={{marginTop:16,borderTop:`1px solid ${C.border}`,paddingTop:12}}>
            <div style={{fontSize:11,fontWeight:700,marginBottom:6}}>월별 지출 계획선 대비 실적</div>
            <svg viewBox="0 0 100 50" style={{width:"100%",height:100}}>
              <line x1={0} y1={0} x2={100} y2={0} stroke="transparent"/>
              {data.지출계.map((v,i)=>{
                const planV = 지출계;
                const mx = Math.max(...data.지출계,planV)*1.2;
                const x=(i+.5)*(100/mc); const bw=100/(mc*1.6);
                const h=(v/mx)*42;
                return <g key={i}><rect x={x-bw/2} y={45-h} width={bw} height={h} fill={v>planV?C.red:C.green} rx={2} opacity={i===mo?1:.55}><title>{ML[i]}: {fmt(v)}</title></rect></g>;
              })}
              <line x1={0} y1={45-(지출계/Math.max(...data.지출계,지출계)/1.2*42)} x2={100} y2={45-(지출계/Math.max(...data.지출계,지출계)/1.2*42)} stroke={C.red} strokeWidth={.5} strokeDasharray="2,1.5"/>
              <text x={98} y={45-(지출계/Math.max(...data.지출계,지출계)/1.2*42)-1.5} textAnchor="end" fontSize={3} fill={C.red}>계획 {fmt(지출계)}</text>
              <line x1={0} y1={45} x2={100} y2={45} stroke={C.border} strokeWidth={.3}/>
            </svg>
          </div>
        </Card>
      </div>
    </div>
  );
}

function TabYoY({d25,d26}) {
  // Compare same months (Jan, Feb)
  const commonM = Math.min(d25.mc, d26.mc); // 2
  
  const compare = (label, arr25, arr26) => {
    return Array(commonM).fill(0).map((_,i) => ({
      month: i+1, v25: arr25[i]||0, v26: arr26[i]||0,
      diff: (arr26[i]||0)-(arr25[i]||0),
      pct: arr25[i] ? ((arr26[i]||0)-(arr25[i]||0))/arr25[i]*100 : 0
    }));
  };

  const inc = compare("수입",d25.수입계,d26.수입계);
  const sav = compare("저축",d25.저축계,d26.저축계);
  const exp = compare("지출",d25.지출계,d26.지출계);
  const free = compare("여유",d25.여유,d26.여유);

  // Category comparison
  const allCats = [...new Set([...Object.keys(d25.순지출),...Object.keys(d26.순지출)])];
  const catComp = allCats.map(cat => {
    const avg25 = d25.순지출[cat] ? S(d25.순지출[cat].slice(0,commonM))/commonM : 0;
    const avg26 = d26.순지출[cat] ? S(d26.순지출[cat].slice(0,commonM))/commonM : 0;
    return {cat, avg25, avg26, diff:avg26-avg25, pct:avg25?(avg26-avg25)/avg25*100:0};
  }).filter(x=>x.avg25>0||x.avg26>0).sort((a,b)=>b.diff-a.diff);

  // Annual averages
  const avg25Inc = S(d25.수입계)/d25.mc, avg26Inc = S(d26.수입계)/d26.mc;
  const avg25Exp = S(d25.지출계)/d25.mc, avg26Exp = S(d26.지출계)/d26.mc;
  const avg25Sav = S(d25.저축계)/d25.mc, avg26Sav = S(d26.저축계)/d26.mc;
  const avg25Free = S(d25.여유)/d25.mc, avg26Free = S(d26.여유)/d26.mc;

  return (
    <div>
      {/* Annual average KPIs */}
      <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10,marginBottom:14}}>
        {[
          {l:"월평균 수입",v25:avg25Inc,v26:avg26Inc,c:C.green,icon:"💵"},
          {l:"월평균 저축",v25:avg25Sav,v26:avg26Sav,c:C.blue,icon:"🏦"},
          {l:"월평균 지출",v25:avg25Exp,v26:avg26Exp,c:C.amber,icon:"💳"},
          {l:"월평균 여유",v25:avg25Free,v26:avg26Free,c:avg26Free>=0?C.cyan:C.red,icon:"✨"},
        ].map((x,i)=>{
          const d=x.v26-x.v25; const dp=x.v25?(d/x.v25*100):0;
          const isExp=x.l.includes("지출"); const good=isExp?d<=0:d>=0;
          return (
            <Card key={i}>
              <div style={{fontSize:9,color:C.t3,fontWeight:600,textTransform:"uppercase"}}>{x.icon} {x.l}</div>
              <div style={{display:"flex",alignItems:"baseline",gap:6,margin:"4px 0"}}>
                <span style={{fontSize:12,color:C.t4,fontFamily:"monospace",textDecoration:"line-through"}}>{fmt(x.v25)}</span>
                <span style={{fontSize:8,color:C.t4}}>→</span>
                <span style={{fontSize:17,fontWeight:800,color:x.c,fontFamily:"monospace"}}>{fmt(x.v26)}</span>
              </div>
              <div style={{fontSize:10,fontWeight:600,color:good?C.green:C.red}}>
                {d>=0?"▲":"▼"} {Math.abs(dp).toFixed(0)}% ({d>=0?"+":""}{fmt(d)})
              </div>
            </Card>
          );
        })}
      </div>

      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:14,marginBottom:14}}>
        {/* Monthly comparison bar chart */}
        <Card>
          <div style={{fontSize:13,fontWeight:700,marginBottom:4}}>동월 비교 (1~{commonM}월)</div>
          <div style={{fontSize:10,color:C.t4,marginBottom:12}}>2025 vs 2026 같은 월 비교</div>
          {[{l:"수입",d:inc,c:C.green},{l:"저축",d:sav,c:C.blue},{l:"지출",d:exp,c:C.amber},{l:"여유",d:free,c:C.cyan}].map((g,gi)=>(
            <div key={gi} style={{marginBottom:12}}>
              <div style={{fontSize:11,fontWeight:600,color:C.t2,marginBottom:4}}>{g.l}</div>
              {g.d.map((r,ri)=>{
                const mx=Math.max(r.v25,r.v26,1)*1.2;
                const isExp=g.l==="지출"; const good=isExp?r.diff<=0:r.diff>=0;
                return (
                  <div key={ri} style={{display:"flex",alignItems:"center",gap:6,marginBottom:3,fontSize:10}}>
                    <span style={{width:24,color:C.t4,fontWeight:600}}>{r.month}월</span>
                    <div style={{flex:1,display:"flex",flexDirection:"column",gap:2}}>
                      <div style={{display:"flex",alignItems:"center",gap:4}}>
                        <div style={{height:8,width:(r.v25/mx*100)+"%",background:g.c,opacity:.35,borderRadius:3}}/>
                        <span style={{fontSize:9,color:C.t4}}>'25 {fmt(r.v25)}</span>
                      </div>
                      <div style={{display:"flex",alignItems:"center",gap:4}}>
                        <div style={{height:8,width:(r.v26/mx*100)+"%",background:g.c,borderRadius:3}}/>
                        <span style={{fontSize:9,fontWeight:600}}>'26 {fmt(r.v26)}</span>
                      </div>
                    </div>
                    <span style={{width:50,textAlign:"right",fontWeight:600,fontSize:9,color:good?C.green:C.red}}>
                      {r.pct>=0?"+":""}{r.pct.toFixed(0)}%
                    </span>
                  </div>
                );
              })}
            </div>
          ))}
        </Card>

        {/* Category YoY comparison */}
        <Card>
          <div style={{fontSize:13,fontWeight:700,marginBottom:4}}>지출 카테고리별 YoY 변화</div>
          <div style={{fontSize:10,color:C.t4,marginBottom:10}}>1~{commonM}월 월평균 기준</div>
          {catComp.map((x,i)=>{
            const mx = Math.max(...catComp.map(c=>Math.max(c.avg25,c.avg26)),1);
            const up = x.diff>0;
            return (
              <div key={i} style={{padding:"6px 0",borderBottom:`1px solid ${C.border}`}}>
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:3}}>
                  <span style={{fontSize:11,fontWeight:600,display:"flex",alignItems:"center",gap:5}}>
                    <span style={{width:8,height:8,borderRadius:"50%",background:CL[x.cat]||"#94a3b8"}}/>
                    {x.cat}
                  </span>
                  <span style={{fontSize:10,fontWeight:600,color:up?C.red:C.green}}>
                    {up?"▲":"▼"} {Math.abs(x.pct).toFixed(0)}%
                  </span>
                </div>
                <div style={{display:"flex",gap:4,alignItems:"center"}}>
                  <div style={{flex:1}}>
                    <div style={{height:6,background:CL[x.cat]||"#94a3b8",opacity:.3,borderRadius:3,width:(x.avg25/mx*100)+"%"}}/>
                    <div style={{height:6,background:CL[x.cat]||"#94a3b8",borderRadius:3,width:(x.avg26/mx*100)+"%",marginTop:2}}/>
                  </div>
                  <div style={{fontSize:9,textAlign:"right",width:80}}>
                    <div style={{color:C.t4}}>'25 {fmt(x.avg25)}</div>
                    <div style={{fontWeight:600}}>'26 {fmt(x.avg26)}</div>
                  </div>
                </div>
              </div>
            );
          })}
        </Card>
      </div>

      {/* Key YoY Insights */}
      <Card>
        <div style={{fontSize:13,fontWeight:700,marginBottom:10}}>💡 연도 비교 핵심 인사이트</div>
        <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:10}}>
          {(() => {
            const insights = [];
            const incChg = avg25Inc ? (avg26Inc-avg25Inc)/avg25Inc*100 : 0;
            insights.push({
              icon: incChg>0?"📈":"📉",
              title: `수입 ${incChg>0?"+":""}${incChg.toFixed(0)}% 변화`,
              body: `월평균 수입이 ${fmt(avg25Inc)}에서 ${fmt(avg26Inc)}으로 ${incChg>0?"증가":"감소"}했습니다.`,
              color: incChg>0?C.green:C.red
            });
            const expChg = avg25Exp ? (avg26Exp-avg25Exp)/avg25Exp*100 : 0;
            insights.push({
              icon: expChg>0?"⚠️":"✅",
              title: `지출 ${expChg>0?"+":""}${expChg.toFixed(0)}% 변화`,
              body: `월평균 지출이 ${fmt(avg25Exp)}에서 ${fmt(avg26Exp)}으로 ${expChg>0?"증가":"감소"}했습니다.`,
              color: expChg>0?C.red:C.green
            });
            const savRate25 = pctN(avg25Sav,avg25Inc), savRate26 = pctN(avg26Sav,avg26Inc);
            insights.push({
              icon: savRate26>savRate25?"💪":"📉",
              title: `저축률 ${savRate25.toFixed(0)}% → ${savRate26.toFixed(0)}%`,
              body: `수입 대비 저축 비율이 ${savRate26>savRate25?"개선":"하락"}되었습니다.`,
              color: savRate26>savRate25?C.green:C.amber
            });
            return insights.map((ins,i)=>(
              <div key={i} style={{background:"#f8f9fb",borderRadius:10,padding:12,borderLeft:`3px solid ${ins.color}`}}>
                <div style={{fontSize:11,fontWeight:700,marginBottom:3}}>{ins.icon} {ins.title}</div>
                <div style={{fontSize:10,color:C.t3,lineHeight:1.5}}>{ins.body}</div>
              </div>
            ));
          })()}
        </div>
      </Card>
    </div>
  );
}

function TabExpenseTable({data,yr,mo}) {
  const grandTotal = S(data.지출계);
  return (
    <Card style={{overflowX:"auto"}}>
      <div style={{fontSize:13,fontWeight:700,marginBottom:10}}>{yr}년 지출 상세 내역</div>
      <table style={{width:"100%",borderCollapse:"collapse",fontSize:10}}>
        <thead>
          <tr style={{borderBottom:`2px solid ${C.border}`}}>
            <th style={{textAlign:"left",padding:"5px 6px",color:C.t3,fontSize:9,fontWeight:600}}>항목</th>
            {Array(data.mc).fill(0).map((_,i)=><th key={i} style={{textAlign:"right",padding:"5px 3px",color:C.t3,fontSize:9,fontWeight:600,background:mo===i?"#f0f0ff":"transparent"}}>{i+1}월</th>)}
            <th style={{textAlign:"right",padding:"5px 6px",fontSize:9,fontWeight:700,color:C.t2}}>계</th>
            <th style={{textAlign:"right",padding:"5px 6px",fontSize:9,fontWeight:600,color:C.t3}}>비중</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(data.순지출).map(([cat,arr])=>{
            const t=S(arr);
            return (
              <tr key={cat} style={{borderBottom:`1px solid #f5f5f5`}}>
                <td style={{padding:"4px 6px",fontWeight:600,color:C.t2,whiteSpace:"nowrap"}}>
                  <span style={{display:"inline-block",width:7,height:7,borderRadius:"50%",background:CL[cat]||"#94a3b8",marginRight:5,verticalAlign:"middle"}}/>{cat}
                </td>
                {arr.map((v,i)=><td key={i} style={{padding:"4px 3px",textAlign:"right",fontFamily:"monospace",fontSize:9,color:v?"#333":"#ddd",background:mo===i?"#f0f0ff":"transparent"}}>{v?fmtK(v):"—"}</td>)}
                <td style={{padding:"4px 6px",textAlign:"right",fontWeight:700,fontFamily:"monospace",fontSize:9}}>{fmtK(t)}</td>
                <td style={{padding:"4px 6px",textAlign:"right",color:C.t3,fontSize:9}}>{pct(t,grandTotal)}</td>
              </tr>
            );
          })}
          <tr style={{borderTop:`2px solid ${C.border}`,background:"#fafafa"}}>
            <td style={{padding:"5px 6px",fontWeight:800}}>합계</td>
            {data.지출계.map((v,i)=><td key={i} style={{padding:"5px 3px",textAlign:"right",fontWeight:700,fontFamily:"monospace",fontSize:9,color:C.amber,background:mo===i?"#f0f0ff":"transparent"}}>{fmtK(v)}</td>)}
            <td style={{padding:"5px 6px",textAlign:"right",fontWeight:800,fontFamily:"monospace",fontSize:9,color:C.red}}>{fmtK(grandTotal)}</td>
            <td style={{padding:"5px 6px",textAlign:"right",fontWeight:700,fontSize:9}}>100%</td>
          </tr>
        </tbody>
      </table>
    </Card>
  );
}

// ════════════════════════════════════════
// APP
// ════════════════════════════════════════
export default function App() {
  const [yr, setYr] = useState(2026);
  const [mo, setMo] = useState(1);
  const [tab, setTab] = useState("overview");

  const d25 = useMemo(()=>proc(RAW[2025]),[]);
  const d26 = useMemo(()=>proc(RAW[2026]),[]);
  const data = yr===2025?d25:d26;
  const vm = Math.min(mo, data.mc-1);

  return (
    <div style={{fontFamily:"'Pretendard','Noto Sans KR',-apple-system,sans-serif",background:C.bg,minHeight:"100vh",padding:"20px 16px",color:C.t1,maxWidth:1100,margin:"0 auto"}}>
      
      <div style={{marginBottom:16}}>
        <h1 style={{fontSize:22,fontWeight:900,margin:0,background:"linear-gradient(135deg,#1a1a2e,#6366f1)",WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent"}}>가계부 동적 인사이트</h1>
        <p style={{color:C.t3,fontSize:12,margin:"3px 0 0"}}>상은 · 아영 부부합산 | 계획 대비 실적 · 연도 비교 · 월별 분석</p>
      </div>

      {/* Top nav */}
      <div style={{display:"flex",gap:8,alignItems:"center",marginBottom:12,flexWrap:"wrap"}}>
        <Tabs items={[{key:2025,label:"2025년"},{key:2026,label:"2026년"}]} active={yr} onChange={v=>{setYr(v);setMo(0);}}/>
        <div style={{width:1,height:22,background:"#ddd"}}/>
        <Tabs items={Array((yr===2025?d25:d26).mc).fill(0).map((_,i)=>({key:i,label:`${i+1}월`}))} active={vm} onChange={setMo} size="sm"/>
      </div>

      {/* Tab nav */}
      <div style={{display:"flex",gap:2,marginBottom:16,borderBottom:`2px solid ${C.border}`,paddingBottom:0}}>
        {[
          {key:"overview",label:"📊 월간 분석"},
          {key:"plan",label:"📋 계획 vs 실적"},
          {key:"yoy",label:"📈 2025 vs 2026"},
          {key:"table",label:"📝 상세 내역"},
        ].map(t=>(
          <button key={t.key} onClick={()=>setTab(t.key)} style={{padding:"8px 18px",border:"none",background:"transparent",cursor:"pointer",fontWeight:600,fontSize:12,
            color:tab===t.key?C.blue:C.t3,borderBottom:`2px solid ${tab===t.key?C.blue:"transparent"}`,marginBottom:-2,transition:"all .15s"}}>{t.label}</button>
        ))}
      </div>

      {/* Content */}
      {tab==="overview" && <TabOverview data={data} yr={yr} mo={vm}/>}
      {tab==="plan" && <TabPlanVsActual data={data} yr={yr} mo={vm}/>}
      {tab==="yoy" && <TabYoY d25={d25} d26={d26}/>}
      {tab==="table" && <TabExpenseTable data={data} yr={yr} mo={vm}/>}

      <div style={{textAlign:"center",fontSize:10,color:C.t4,marginTop:24,padding:8}}>가계부 동적 인사이트 v2.0 · {new Date().toLocaleDateString("ko-KR")} 기준</div>
    </div>
  );
}
