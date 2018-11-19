#-*-coding:utf-8-*-
import visdom
# vis = visdom.Visdom(env=args.visname)
# vis.line(X=torch.FloatTensor([0]), Y=torch.FloatTensor([0]), win='loss', update='append')
# vis.line(X=torch.FloatTensor([0]), Y=torch.FloatTensor([0]), win='train_accuracy', update='append')
# vis.line(X=torch.FloatTensor([0]), Y=torch.FloatTensor([0]), win='val_accuracy', update='append')


## in trainer.py
def train_epoch(model, num_batches, train_loader, print_freq, optimizer=None, vis=None):
    criterion = torch.nn.CrossEntropyLoss()
    for batch, label in train_loader:
        loss = train_batch(model, optimizer, batch.cuda(), label.cuda(), criterion)
        if num_batches%print_freq == 0:
            print('%23s%-9s%-13s'%('the '+str(num_batches)+'th batch, ','loss is: ',str(round(loss,8))))
        num_batches +=1
        if vis:
            vis.line(X=torch.FloatTensor([num_batches]), Y=torch.FloatTensor([float(loss.cpu())]), win='loss', update='append')
    return num_batches
