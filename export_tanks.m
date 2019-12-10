clear
%%
clc
tname = 'AHCW_191119';
sourcedir = 'Z:\Calvin\data transfer folder\';
tankpath = fullfile(sourcedir,tname);

a=dir(tankpath);
an={a.name}';
% al=cat(1,a.isdir)&~contains(an,'.')&(contains(an,'rec')|cellfun(@length,an)==9);
al=cat(1,a.isdir)&~contains(an,'.');
allblocks = an(al);

%
savedir = '\\maize.umhsnas.med.umich.edu\KHRI-SES-Lab\Calvin\Analysis\dcn_immediate\CW_GP_191119';
if ~exist(savedir)
    mkdir(savedir);
end

b=what(savedir);
bn=cellfun(@(x) x(1:end-4),b.mat,'uniformoutput',0);
allblocks = allblocks(~ismember(allblocks,bn));


%% read tank
for i=1:length(allblocks)
    clear data
    block=allblocks{i};
    tic;
    fprintf('Accessing %s...\n',block)
    data=TDT2mat(tankpath,block,'verbose',0);
    fprintf('Saving...\n')
    save(fullfile(savedir,block),'data','-v7.3')
    timestop=toc;
    fprintf('%s saved (%d/%d); %.2f sec\n',block,i,length(allblocks),timestop)
end
%%
fprintf('Done.\n')

