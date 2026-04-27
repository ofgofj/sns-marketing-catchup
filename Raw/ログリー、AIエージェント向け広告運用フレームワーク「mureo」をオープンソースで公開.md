---
title: "ログリー、AIエージェント向け広告運用フレームワーク「mureo」をオープンソースで公開"
source: "https://markezine.jp/article/detail/50588"
published: Thu, 23 Apr 2026 11:30:00 +0900
tags:
  - clippings
---

MarkeZineニュース
            
      
    

    ログリー、AIエージェント向け広告運用フレームワーク「mureo」をオープンソースで公開
        
      
                                                            MarkeZine編集部[著]
                              
            2026/04/23 11:30
          
    
      
        
                    ニュース
                    運用型広告
                    AI
                    ITサービス
                  
      
      
        
    
if (location.protocol == "https:") {
  (function(p,u,s,h) {
       p._pcq = p._pcq || [];
       p._pcq.push(['_currentTime', Date.now()]);
       p._pcq.push(['noTrigger', true]);
       s = u.createElement('script'); s.type = 'text/javascript'; s.async = true;
       s.src = 'https://cdn.pushcrew.com/js/ab0eed88487fddca11873aa5a7d349ba.js';
       h = u.getElementsByTagName('script')[0]; h.parentNode.insertBefore(s, h);
  })(window,document);

  _pcq.push(['APIReady', callbackFunction]);
}

function callbackFunction() {
  if (pushcrew.subscriberId == false) {
    $('#push_button').html('プッシュ通知ON');
    $('#push_slide_button').removeClass('is-active');
  } else if (!pushcrew.subscriberId) {
    $('#push_button').html('プッシュ通知ON');
    $('#push_slide_button').removeClass('is-active');
  } else if (pushcrew.subscriberId == -1) {
    $('#push_button').html('プッシュ通知ON');
    $('#push_slide_button').removeClass('is-active');
  } else {
    $('#push_button').html('プッシュ通知OFF');
    $('#push_slide_button').addClass('is-active');
  }
}


            
  
    
    
        
          通知
      
      
    
  

  
    

      

                        
    

    
                                          　ログリーは、AIエージェント向け広告運用フレームワーク「mureo（ムレオ）」を、Apache License 2.0のもとオープンソースソフトウェアとして公開した。「mureo」は、Google広告やMeta広告、Google Search Console、Google Analytics 4（GA4）など複数の広告媒体や解析ツールを横断し、AIエージェントが自律的に広告アカウント運用を支援するフレームワークだ。



　生成AIの進展にともない広告運用でAIエージェント活用が進む一方、既存AIツールは単発のタスクが中心で、ビジネス戦略や担当者のノウハウを反映した継続運用には課題があったと同社は指摘。これに対し「mureo」は、ユーザーのビジネス戦略やペルソナ、KPIを起点に意思決定ができる仕組みを提供するもの。広告コピー作成や予算配分まで、一貫したブランド方針に基づくAI運用が可能となる。

　媒体横断のデータ統合や相関分析を自動化し、広告・自然検索・サイト行動を踏まえた多角的な運用改善ができるほか、熟練担当者の判断基準や運用ナレッジもワークフローに組み込まれ、AI初導入の現場もスムーズに運用を始められる点を特長としている。さらに、運用データへの知見をAIが学習し続け、使い込むほど組織ごとの方針に合わせた運用が実現する。

　セキュリティにも配慮し、認証情報の隔離やリアルタイム異常検知、ポリシーチェックなど多層防御を実装。広告アカウントをAIに任せつつも、最終的な判断は人間が担える設計とした。

　今後はオープンソースコミュニティのフィードバックも取り入れ、対応媒体追加や多言語対応など機能強化を進める方針である。

【関連記事】
・サイバーエージェント、広告配信運用AIエージェント「効果おまかせAI」を提供へ　入札・配信を最適化
・AI自動運用型インフルエンサー広告サービス「Vooster」、新たに「TikTok」連携を開始
・楽天、データとAI活用のマーケティングソリューションを発表　運用型TVCMは4月～試験運用を開始予定
・デジタルガレージ、AIパッケージ「DG AI Drive」提供　広告運用とビジュアル制作を自動化
・セプテーニ子会社、ディスプレイ広告運用自動化システム「ADPILOT」の提供を開始
                        


    

              
     

    
    
        
    
    
      var cX = window.cX = window.cX || {}; cX.callQueue = cX.callQueue || [];
      cX.CCE = cX.CCE || {}; cX.CCE.callQueue = cX.CCE.callQueue || [];
      cX.CCE.callQueue.push(['run',{
        widgetId: '25d1c912f531254981e4c885b8fea221510a6eb6',
        targetElementId: 'cx_25d1c912f53125
