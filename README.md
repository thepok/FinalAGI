# FinalAGI

At the Moment development is in a jupiter file named ProtoOne.

The Agent is based on a more sophisticated Task Pool concept. The Tasks are connected in a Graph. There a Parent and Child Tasks...
more info in the notebook

## Planned Phases
### Heavy guided phase
Agent recives guidens by human user in planning and execution phase
### Light guiding
Agent only recives guidence in the planning phase
### full autonomy
Agent searches autonome to improvments of his problemsolving capapilities and tests them


## Ideas and TODOs
Allways perform a langchsin compress retriever step over available information.

Task tree should be at the heart. 

Smallest unit of work:
Compress->select tools->think->improve->act commands->describe current state

Task description and prompts in the eli5 format. But use 12 or so

Add curent list of fils allways in problem solver promp with their stats like pagecount

Add local CoT and reflection step in solver

Tell it that looking at file means iterating over it

Split function dissolves main task. Maybe call function that creates result description when all child's done


Add curent list of fils allways in problem solver promp with their stats like pagecount

create a Task complexity evaluation (maybe arround number of expected commands needed) and use this to split tasks

agent needs a portfolio of suggested workflows that help to handle the small contextsize.
    explain how to read big files page by page
    write novels chapter by chapter and keep a file containing current state of the novel(where wich person is and so on) that changes after every new text written


remove oldest messages when contextwindow gets full in task solver

## Problems
It "copies" a file but halucinates extra contend into it 